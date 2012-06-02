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
        self.socket.send("idAck")
    def postEvent(self, event, data):
        self.socket.send(pickle.dumps(utils.netEvent(event, data), 2))
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
        self.setResponse("spawnEntity", self.ev_spawnEntity)
        self.setResponse("distLevel", self.ev_distLevel)
        self.setResponse("distSwitchLevel", self.ev_distSwitchLevel)
        self.setResponse("update", self.ev_update)
        self.reg("kill", self)
        self.reg("getLevel", self)
        self.reg("spawnEntity", self)
        self.manager.reg("distLevel", self)
        self.manager.reg("distSwitchLevel", self)
        self.manager.reg("update", self)
        self.client = clientWrapper(clientsocket)
        self.dbWrap = db.entityDBWrapper("entity.db")
        self.plugins = []
        try:
            self.controlledEntity = self.dbWrap.fetchEntity(self.client.avatarID, self.manager)
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
    def ev_update(self, data):
        self.alert(chameleon.event("update", None))
    #@utils.trace
    def ev_kill(self, data):
        print "KILL!"
        self.client.close()
        self.unregister("kill", self)
        self.manager.unregister("update", self)
        self.plugins = []
        self.manager.alert(chameleon.event("removeNetSubsystem", self))
        self.dbWrap.saveEntity(self.controlledEntity)
        self.controlledEntity.kill()
    #@utils.trace
    def ev_getLevel(self, data):
        self.manager.alert(chameleon.event("getLevel", self.controlledEntity))
    #@utils.trace
    def ev_spawnEntity(self, data):
        self.manager.alert(chameleon.event("spawnEntity", data))
    #@utils.trace
    def ev_distSwitchLevel(self, data):
        print data
        if data[1] == self.controlledEntity.data["name"]:
            print "switch"
            self.controlledEntity.kill()
            self.controlledEntity.data["coords"] = data[0].startcoords
            self.controlledEntity.rect = pygame.rect.Rect(self.controlledEntity.data["coords"], (50, 50))
            self.manager.alert(chameleon.event("spawnEntity", (self.controlledEntity, self.controlledEntity.curLevel)))
            print "after alert spawn entity"
            self.alert(chameleon.event("distLevel", data[0]))
            self.alert(chameleon.event("updateBlockState", None))
    #@utils.trace
    def ev_distLevel(self, data):
        if data[1] == self.controlledEntity.data["name"]:
                self.alert(chameleon.event("distLevel", data[0]))
class networkView(chameleon.listener):
    def __init__(self, manager, client):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("update", self.ev_update)
        self.setResponse("distLevel", self.ev_distLevel)
        self.setResponse("sendBlockState", self.ev_sendBlockState)
        self.setResponse("ackBlockState", self.ev_ackBlockState)
        self.setResponse("updateBlockState", self.ev_updateBlockState)
        self.manager.reg("update", self)
        self.manager.reg("distLevel", self)
        self.manager.reg("sendBlockState", self)
        self.manager.reg("ackBlockState", self)
        self.manager.reg("updateBlockState", self)
        self.client = client
        self.level = None
        self.manager.alert(chameleon.event("getLevel", None))
        self.manager.alert(chameleon.event("sendBlockState", None))
        self.needsToSend = False
    #@utils.trace
    def ev_update(self, data):
        try:
            self.client.postEvent("entityPosReceived", self.level.entityState.serialize())
            if self.needsToSend:
                self.manager.alert(chameleon.event("sendBlockState", None))
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    #@utils.trace
    def ev_sendBlockState(self, data):
        try:
            self.client.postEvent("blockStateReceived", self.level.blockState.serialize())
        except IOError:
            self.manager.alert(chameleon.event("kill", None))
    def ev_ackBlockState(self, data):
        print "ackBlockState"
        self.needsToSend = False
    def ev_updateBlockState(self, data):
        self.needsToSend = True
    def ev_distLevel(self, data):
        print "distribute level"
        self.level = data
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
        self.levelManager = levelManager(self)
        self.netSubDelegator = networkSubsystemDelegator(self)
        self.scheduleQueue = []
    def main(self):
        while 1:
            self.alert(chameleon.event("update", None))
manager = spinner()
def run():
    """We need this method to expose manager.main() to runserver.py in an appealing manner."""
    manager.main()
