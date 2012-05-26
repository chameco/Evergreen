from .. import base
from .. import utils
from .. import level
from .. import errors
from .. import net # Net is mostly obsolete, but we need net.netEvent
from .. import chameleon
from . import db
import sys
import os
import cPickle as pickle
import socket
import ConfigParser
import select
import time
import atexit
import pygame
pygame.init()
CONFIG = {}
CONFIG["basedir"] = os.path.abspath(".")
CONFIG["packagedir"] = os.path.join(CONFIG["basedir"], "src")
CONFIG["serverdir"] = os.path.join(CONFIG["packagedir"], "server")
configParser = ConfigParser.ConfigParser()
configParser.read(os.path.join(CONFIG["serverdir"], "server.ini"))
CONFIG["maxplayers"] = configParser.getint("core", "maxplayers")
CONFIG["port"] = configParser.getint("network", "port")
CONFIG["levelpack"] = configParser.get("core", "levelpack")
CONFIG["plugins"] = configParser.items("plugins")
class clientWrapper():
    def __init__(self, clientsocket):
        self.socket = clientsocket
        self.poll = select.poll()
        self.poll.register(self.socket, select.POLLIN)
        self.avatarID = self.socket.recv(256)
        print self.avatarID
        self.socket.send("idAck")
    def postEvent(self, event, data):
        #print event
        #print data
        self.socket.send(pickle.dumps(net.netEvent(event, data), 2))
    def getData(self):
        #print "getData"
        request = ""
        while self.poll.poll(0):
            request += self.socket.recv(8192)
            #print request
        if request != "":
            return pickle.loads(request).cham()
        return None
    def close(self):
        self.socket.close()
class networkSubsystem(chameleon.manager, chameleon.listener):
    """
        networkSubsystem is a private manager class, one is instantiated for each client.
        Be careful - Anything may and will be called multiple times.
    """
    def __init__(self, manager, clientsocket):
        chameleon.manager.__init__(self)
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("kill", self.ev_kill)
        self.setResponse("getLevel", self.ev_getLevel)
        #self.setResponse("getEntityState", self.ev_getEntityState)
        self.setResponse("spawnEntity", self.ev_spawnEntity)
        self.setResponse("distLevel", self.ev_distLevel)
        #self.setResponse("distEntityState", self.ev_distEntityState)
        self.setResponse("update", self.ev_update)
        self.reg("kill", self)
        self.reg("getLevel", self)
        #self.reg("getEntityState", self)
        self.reg("spawnEntity", self)
        self.manager.reg("distLevel", self)
        #self.manager.reg("distEntityState", self)
        self.manager.reg("update", self)
        self.client = clientWrapper(clientsocket)
        self.dbWrap = db.entityDBWrapper("entity.db")
        self.plugins = []
        self.killFlag = False
        self.firstLevelFlag = True
        try:
            self.controlledEntity = self.dbWrap.fetchEntity(self.client.avatarID, self)
        except errors.dbError as e:
            print "Unknown character"
            self.alert(chameleon.event("kill", None))
        else:
            self.manager.alert(chameleon.event("spawnEntity", (self.controlledEntity, self.controlledEntity.curLevel)))
            self.plugins.append(networkController(self, self.client))
            self.plugins.append(networkView(self, self.client))
            print CONFIG
            for plugin, option in CONFIG["plugins"]:
                if option:
                    exec("from plugins import " + plugin)
                    exec("plugin = " + plugin + "." + plugin)
                    self.registerPlugin(plugin)
            print self.plugins
    def registerPlugin(self, plugin):
        self.plugins.append(plugin(self, self.controlledEntity))
    def alertUp(self, event):
        self.manager.alert(event)
    def ev_update(self, data):
        self.alert(chameleon.event("update", None))
    def ev_kill(self, data):
        if not self.killFlag:#We need extra precautions if unregistering while alerting.
            print "KILL!"
            self.client.close()
            self.manager.unregister("update", self)
            self.manager.unregister("kill", self)
            self.setResponse("update", utils.sponge)
            self.setResponse("kill", utils.sponge)
            self.plugins = []
            self.manager.alert(chameleon.event("removeNetSubsystem", self))
            self.dbWrap.saveEntity(self.controlledEntity)
            self.controlledEntity.kill()
            self.killFlag = True
    def ev_getLevel(self, data):
        self.manager.alert(chameleon.event("getLevel", self.controlledEntity.curLevel))
    def ev_spawnEntity(self, data):
        self.manager.alert(chameleon.event("spawnEntity", data))
    def ev_distLevel(self, data):
        if data[1] == self.controlledEntity.curLevel and self.firstLevelFlag == False and not data:
            print "switch"
            self.controlledEntity.kill()
            self.controlledEntity.data["coords"] = data[0].startcoords
            self.controlledEntity.rect = pygame.rect.Rect(self.controlledEntity.data["coords"], (50, 50))
            self.manager.alert(chameleon.event("spawnEntity", (self.controlledEntity, self.controlledEntity.curLevel)))
            self.alert(chameleon.event("distLevel", data[0]))
            self.alert(chameleon.event("sendBlockState", None))
        else:
            self.controlledEntity.data["coords"] = data[0].startcoords
            self.controlledEntity.rect = pygame.rect.Rect(self.controlledEntity.data["coords"], (50, 50))
            self.alert(chameleon.event("distLevel", data[0]))
            self.alert(chameleon.event("sendBlockState", None))
            self.firstLevelFlag = False
    def ev_distEntityState(self, data):
        if data[1] == self.controlledEntity.curLevel:
            self.alert(chameleon.event("distEntityState", data[0]))
class networkView(chameleon.listener):
    def __init__(self, manager, client):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("update", self.ev_update)
        self.setResponse("distLevel", self.ev_distLevel)
        self.setResponse("sendBlockState", self.ev_sendBlockState)
        self.manager.reg("update", self)
        self.manager.reg("distLevel", self)
        self.manager.reg("sendBlockState", self)
        self.client = client
        self.level = None
        self.manager.alert(chameleon.event("getLevel", None))
    def ev_update(self, data):
        try:
            self.client.postEvent("entityPosReceived", self.level.entityState.serialize())
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    def ev_sendBlockState(self, data):
        try:
            self.client.postEvent("initialStateReceived", self.level.blockState.serialize())
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    def ev_distLevel(self, data):
        print "Distribute Level"
        self.level = data
class networkController(chameleon.listener):
    def __init__(self, manager, client):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("update", self.ev_update)
        self.manager.reg("update", self)
        self.client = client
    def ev_update(self, data):
        try:
            data = self.client.getData()
        except errors.netError:
            self.manager.alert(chameleon.event("kill", None))
        except socket.error:
            self.manager.alert(chameleon.event("kill", None))
        if data:
            #print data.name, data.data
            self.manager.alert(data)
class networkSubsystemDelegator(chameleon.listener):
    def __init__(self, manager):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("update", self.ev_update)
        self.setResponse("removeNetSubsystem", self.ev_removeNetSubsystem)
        self.manager.reg("update", self)
        self.manager.reg("removeNetSubsystem", self)
        self.netSubsystems = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", CONFIG["port"]))
        self.socket.listen(5)
        atexit.register(self.socket.close)
    def ev_update(self, data):
        if len(self.netSubsystems) <= CONFIG["maxplayers"]:
            if len(select.select([self.socket], [], [], 0)[0]):
                client = self.socket.accept()[0]
                self.netSubsystems.append(networkSubsystem(self.manager, client))
        #print self.netSubsystems
    def ev_removeNetSubsystem(self, data):
        try:
            self.netSubsystems.remove(data)
        except ValueError:
            pass
class spinner(chameleon.manager):
    def __init__(self):
        chameleon.manager.__init__(self)
        exec("from levels." + CONFIG["levelpack"] + " import levelManager")
        self.levelManager = levelManager(self)
        self.netSubDelegator = networkSubsystemDelegator(self)
    def main(self):
        #curtime = time.time()
        while 1:
            self.alert(chameleon.event("update", None))
            #delta = time.time() - curtime
            #if delta >= 0.1:
            #    t = list(self.level.blockState.sprites())
            #    t.extend(self.level.entityState.sprites())
            #    self.level.entityState.update(t)#Need to change this to support collisions with other entities. DO THIS NOW!
            #    curtime = time.time()
manager = spinner()
def run():
    """We need this method to expose manager.main() to runserver.py in an appealing manner."""
    manager.main()
