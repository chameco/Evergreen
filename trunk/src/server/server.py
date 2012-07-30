#Copyright 2011 Samuel Breese. Distributed under the terms of the GNU General Public License.
#This file is part of Evergreen.
#
#    Evergreen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Evergreen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Evergreen.  If not, see <http://www.gnu.org/licenses/>.
import pygame
pygame.init()
from .. import base
from .. import utils
from .. import level
from .. import errors
from . import db
import sys
import os
import cPickle as pickle
import socket
import ConfigParser
import select
import time
import chameleon
import atexit
import logging
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
CONFIG["logfile"] = configParser.get("core", "logfile")
logging.basicConfig(filename=CONFIG["logfile"], level=logging.DEBUG)
class logManager(chameleon.listener):
    def __init__(self, manager):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.log = logging.getLogger("chameleon.server")
        self.setResponse("log", self.ev_log)
        self.manager.reg("log", self)
    def ev_log(self, data):
        self.log.debug(data)
class clientWrapper():
    def __init__(self, clientsocket):
        self.socket = clientsocket
        self.poll = select.poll()
        self.poll.register(self.socket, select.POLLIN)
        self.avatarID = self.socket.recv(256)
        print self.avatarID
    def postEvent(self, event, data):
        self.socket.send(pickle.dumps(utils.netEvent(event, data), 2) + "\xEE")#An unused delimiter character
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
        self.plugins = []
        self.manager = manager
        self.client = clientWrapper(clientsocket)
        self.setResponse("kill", self.ev_kill)
        print "distEntity_" + self.client.avatarID
        self.setResponse("distEntity_" + self.client.avatarID, self.ev_distEntity)
        self.reg("kill", self)
        self.manager.reg("distEntity_" + self.client.avatarID, self)
        try:
            self.manager.alert(chameleon.event("fetchEntity", self.client.avatarID))
        except errors.dbError as e:
            print "Unknown character"
            self.alert(chameleon.event("kill", None))
    def registerPlugin(self, plugin):
        self.plugins.append(plugin(self, self.controlledEntity))
    def ev_distEntity(self, data):
        print "distEntity"
        self.manager.unregister("distEntity_" + self.client.avatarID, self)
        self.controlledEntity = data
        self.setResponse("getLevel", self.ev_getLevel)
        self.setResponse("distLevel", self.ev_distLevel)
        self.setResponse("distSwitchLevel", self.ev_distSwitchLevel)
        self.setResponse("entityMoved", self.ev_entityMoved)
        self.setResponse("entitySpawned", self.ev_entitySpawned)
        self.setResponse("entityKilled", self.ev_entityKilled)
        self.setResponse("update", self.ev_update)
        self.reg("getLevel", self)
        self.manager.reg("distLevel", self)
        self.manager.reg("distSwitchLevel", self)
        self.manager.reg("entityMoved", self)
        self.manager.reg("entitySpawned", self)
        self.manager.reg("entityKilled", self)
        self.manager.reg("update", self)
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
    def ev_update(self, data):
        self.alert(chameleon.event("update", None))
    def ev_kill(self, data):
        print "KILL!"
        self.client.close()
        self.unregister("kill", self)
        self.manager.unregister("update", self)
        self.plugins = []
        self.manager.alert(chameleon.event("removeNetSubsystem", self))
        self.controlledEntity.kill()
        self.manager.alert(chameleon.event("killEntity", self.controlledEntity))
        self.manager.alert(chameleon.event("saveEntity", self.controlledEntity))
    def ev_getLevel(self, data):
        self.manager.alert(chameleon.event("getLevel", self.controlledEntity))
    def ev_distSwitchLevel(self, data):
        print data
        if data[1] == self.controlledEntity.data["name"]:
            print "switch"
            self.controlledEntity.kill()
            self.manager.alert(chameleon.event("killEntity", self.controlledEntity))
            self.controlledEntity.data["coords"] = data[0].startcoords
            self.controlledEntity.rect = pygame.rect.Rect(self.controlledEntity.data["coords"], (32, 32))
            self.manager.alert(chameleon.event("spawnEntity", (self.controlledEntity, self.controlledEntity.curLevel)))
            print "after alert spawn entity"
            self.alert(chameleon.event("distLevel", data[0]))
            self.alert(chameleon.event("sendLevel", None))
    def ev_distLevel(self, data):
        if data[1] == self.controlledEntity.data["name"]:
                self.alert(chameleon.event("distLevel", data[0]))
    def ev_entityMoved(self, data):
        print "entityMoved"
        if data[2] == self.controlledEntity.curLevel:
            self.alert(chameleon.event("entityMoved", (data[0], data[1])))
    def ev_entitySpawned(self, data):
        if data[1] == self.controlledEntity.curLevel:
            self.alert(chameleon.event("entitySpawned", data[0]))
    def ev_entityKilled(self, data):
        print "entityKilled"
        if data[1] == self.controlledEntity.curLevel:
            self.alert(chameleon.event("entityKilled", data[0]))
    def ev_gameOver(self, data):
        print "GAME OVER"
        if data is self.controlledEntity:
            self.alert(chameleon.event("gameOver", None))
class networkView(chameleon.listener):
    def __init__(self, manager, client):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("distLevel", self.ev_distLevel)
        self.setResponse("sendLevel", self.ev_sendLevel)
        self.setResponse("entityMoved", self.ev_entityMoved)
        self.setResponse("entitySpawned", self.ev_entitySpawned)
        self.setResponse("entityKilled", self.ev_entityKilled)
        self.setResponse("gameOver", self.ev_gameOver)
        self.manager.reg("distLevel", self)
        self.manager.reg("sendLevel", self)
        self.manager.reg("entityMoved", self)
        self.manager.reg("entitySpawned", self)
        self.manager.reg("entityKilled", self)
        self.manager.reg("gameOver", self)
        self.client = client
        self.level = None
        self.manager.alert(chameleon.event("getLevel", None))
        self.manager.alert(chameleon.event("sendLevel", None))
    def ev_sendLevel(self, data):
        try:
            self.client.postEvent("levelReceived", (self.level.blockState.serialize(), self.level.floorState.serialize(), self.level.entityState.serialize()))
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    def ev_distLevel(self, data):
        print "distribute level"
        self.level = data
    def ev_entityMoved(self, data):
        try:
            self.client.postEvent("entityMoved", (data[0].serialize(), data[1]))
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    def ev_entitySpawned(self, data):
        try:
            self.client.postEvent("entitySpawned", data.serialize())
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    def ev_entityKilled(self, data):
        print "entityKilled: networkView"
        try:
            self.client.postEvent("entityKilled", data.serialize())
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    def ev_gameOver(self, data):
        print "GAME OVER: networkView"
        try:
            self.client.postEvent("gameOver", None)
        finally:
            self.manager.alert(chameleon.event("kill", None))
class networkController(chameleon.listener):
    def __init__(self, manager, client):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("update", self.ev_update)
        self.manager.reg("update", self)
        self.client = client
    #@utils.trace
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
    #@utils.trace
    def ev_update(self, data):
        if len(self.netSubsystems) <= CONFIG["maxplayers"]:
            if len(select.select([self.socket], [], [], 0)[0]):
                client = self.socket.accept()[0]
                self.netSubsystems.append(networkSubsystem(self.manager, client))
        #print self.netSubsystems
    #@utils.trace
    def ev_removeNetSubsystem(self, data):
        try:
            self.netSubsystems.remove(data)
        except ValueError:
            pass
class spinner(chameleon.manager):
    def __init__(self):
        chameleon.manager.__init__(self)
        if __debug__:
            self.logManager = logManager(self)
        exec("from levels." + CONFIG["levelpack"] + " import levelManager")
        self.dbManager = db.dbManager(self)
        self.levelManager = levelManager(self)
        self.netSubDelegator = networkSubsystemDelegator(self)
    def main(self):
        while 1:
            self.alert(chameleon.event("update", None))
manager = spinner()
def run():
    """We need this method to expose manager.main() to runserver.py in an appealing manner."""
    manager.main()
