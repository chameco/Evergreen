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
import os
import sys
import socket
import collections
import pygame
import cPickle as pickle
import re
import select
import chameleon
import ConfigParser
import argparse
pygame.init()
CONFIG = {}
CONFIG["basedir"] = os.path.abspath(".")
CONFIG["packagedir"] = os.path.join(CONFIG["basedir"], "src")
CONFIG["clientdir"] = os.path.join(CONFIG["packagedir"], "client")
configParser = ConfigParser.ConfigParser()
configParser.read(os.path.join(CONFIG["clientdir"], "client.ini"))
CONFIG["playername"] = configParser.get("player", "name")
CONFIG["port"] = configParser.getint("network", "port")
CONFIG["host"] = configParser.get("network", "host")
CONFIG["fullscreen"] = configParser.getboolean("video", "fullscreen")
CONFIG["spritepack"] = configParser.get("video", "spritepack")
PARSER = argparse.ArgumentParser(description="Launch the Evergreen client")
PARSER.add_argument("--playername", dest="playername", default=CONFIG["playername"], type=str, help="specify player name (overrides the configuration file)")
PARSER.add_argument("--port", dest="port", default=CONFIG["port"], type=int, help="specify server port (overrides the configuration file)")
PARSER.add_argument("--host", dest="host", default=CONFIG["host"], type=str, help="specify server address (overrides the configuration file)")
PARSER.add_argument("--fullscreen", dest="fullscreen", default=CONFIG["fullscreen"], type=int, help="specify whether or not to run in fullscreen (0 or 1, overrides the configuration file)")
PARSER.add_argument("--spritepack", dest="spritepack", default=CONFIG["spritepack"], type=str, help="specify spritepack to use (overrides the configuration file)")
ARGS = PARSER.parse_args()
CONFIG["playername"] = ARGS.playername
CONFIG["port"] = ARGS.port
CONFIG["host"] = ARGS.host
CONFIG["fullscreen"] = ARGS.fullscreen
CONFIG["spritepack"] = ARGS.spritepack
if CONFIG["fullscreen"]:
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
else:
    pygame.display.set_mode()
from .. import base
from .. import level
from .. import errors
from .. import utils
exec("import spritepacks." + CONFIG["spritepack"] + " as spritepack")
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])#Mouse events fill up the queue, causing major lag.
class serverWrapper():
    def __init__(self, serversocket):
        self.socket = serversocket
        self.poll = select.poll()
        self.poll.register(self.socket, select.POLLIN)
        self.socket.send(CONFIG["playername"])
        ack = self.socket.recv(6)
        if ack != "idAck":
            raise errors.serverError("Error: server refuses to acknowledge ID message.")
    def postEvent(self, event, data):
        #print event
        #print data
        self.socket.send(pickle.dumps(utils.netEvent(event, data)), 2)
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
class networkController(chameleon.listener):
    def __init__(self, manager, server):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("blockStateReceived", self.ev_blockStateReceived)
        self.setResponse("entityPosReceived", self.ev_entityPosReceived)
        self.setResponse("update", self.ev_update)
        self.manager.reg("blockStateReceived", self)
        self.manager.reg("entityPosReceived", self)
        self.manager.reg("update", self)
        self.server = server
        self.blockState = None
        self.entityState = None
    def ev_blockStateReceived(self, data):
        print "Block State Received"
        self.blockState = base.copyableGroup.load(data)
        self.manager.alert(chameleon.event("distBlockState", self.blockState))# We do it this way so everyone has the same reference to the newly-loaded state. Probably unnessesary, but I like it.
        self.server.postEvent("ackBlockState", None)
    def ev_entityPosReceived(self, data):
        #print "Entity Positions Received"
        self.entityState = base.copyableGroup.load(data)
        #print self.entityState.sprites()
        self.manager.alert(chameleon.event("distEntityPos", self.entityState))
    def ev_update(self, data):
        #self.server.postEvent("requestEntityPos", None)
        response = self.server.getData()
        #print response
        if response:
            self.manager.alert(response)
class networkView(chameleon.listener):
    def __init__(self, manager, server):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("w", self.ev_w)
        self.setResponse("s", self.ev_s)
        self.setResponse("a", self.ev_a)
        self.setResponse("d", self.ev_d)
        self.setResponse("space", self.ev_space)
        self.setResponse("logout", self.ev_logout)
        self.manager.reg("w", self)
        self.manager.reg("s", self)
        self.manager.reg("a", self)
        self.manager.reg("d", self)
        self.manager.reg("space", self)
        self.manager.reg("logout", self)
        self.server = server
    def ev_w(self, data):
        #print "w"
        self.server.postEvent("up", data)
    def ev_s(self, data):
        #print "s"
        self.server.postEvent("down", data)
    def ev_a(self, data):
        #print "a"
        self.server.postEvent("left", data)
    def ev_d(self, data):
        #print "d"
        self.server.postEvent("right", data)
    def ev_space(self, data):
        self.server.postEvent("attack", data)
    def ev_logout(self, data):
        self.server.postEvent("kill", data)
class keyController(chameleon.listener):
    def __init__(self, manager):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("escape", self.ev_escape)
        self.setResponse("update", self.ev_update)
        self.manager.reg("escape", self)
        self.manager.reg("update", self)
    def ev_update(self, data):
        currentEvent = pygame.event.poll()
        if currentEvent.type == pygame.QUIT: 
            self.manager.alert(chameleon.event("logout", None))
            sys.exit(0)
        elif currentEvent.type == pygame.KEYDOWN:
            self.manager.alert(chameleon.event(pygame.key.name(currentEvent.key), True))
        elif currentEvent.type == pygame.KEYUP:
            self.manager.alert(chameleon.event(pygame.key.name(currentEvent.key), False))
    def ev_escape(self, data):
        self.manager.alert(chameleon.event("logout", None))
        sys.exit(0)
class localStateView(chameleon.listener):
    def __init__(self, manager):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("distBlockState", self.ev_distBlockState)
        self.setResponse("distEntityPos", self.ev_distEntityPos)
        self.setResponse("update", self.ev_update)
        self.manager.reg("distBlockState", self)
        self.manager.reg("distEntityPos", self)
        self.manager.reg("update", self)
        self.blockState = None
        self.char = None
        self.chargroup = pygame.sprite.GroupSingle()
        self.entityState = None
        self.surfBuf = pygame.surface.Surface((5000, 5000)) #We can increase this later.
        self.screen = pygame.display.get_surface()
        self.screenrect = self.screen.get_rect()
        self.clearcallback = lambda surf, rect : surf.fill((0, 0, 0), rect)
    def ev_distBlockState(self, data):
        print "diststate"
        if self.blockState is not None: #This whole section is only called upon level switch, so it's not performance critical.
            print "new blockstate"
            if self.entityState:
                self.entityState.clear(self.surfBuf, self.clearcallback)
                self.entityState = None #Keep entityState from being blit in ev_update.
            self.blockState.clear(self.surfBuf, self.clearcallback)
        self.blockState = data
        for sprite in self.blockState:
            sprite.image = spritepack.getImage(sprite.imgname)
        self.blockState.draw(self.surfBuf) #We need to perform an initial draw here so we don't need extra logic in ev_update for whether or not to call self.state.clear().
    def ev_distEntityPos(self, data):
        if self.entityState:
            self.entityState.clear(self.surfBuf, self.clearcallback)
        self.entityState = data
        for sprite in self.entityState:
            if spritepack.hasEntityImage(sprite.imgname):
                sprite.images = spritepack.getEntityImage(sprite.imgname)
            else:
                sprite.images = spritepack.getEntityImage("entity")
            sprite.image = sprite.images[sprite.data["facing"]][0]
        self.char = [char for char in self.entityState.sprites() if char.data["name"] == CONFIG["playername"]][0]
        self.chargroup.add(self.char)
        self.entityState.draw(self.surfBuf)
        self.chargroup.draw(self.surfBuf)
    def ev_update(self, data):
        if self.entityState:
            self.screenrect.center = self.char.rect.center
            self.chargroup.clear(self.surfBuf, self.clearcallback)
            self.entityState.clear(self.surfBuf, self.clearcallback)
            self.chargroup.draw(self.surfBuf)
            self.entityState.draw(self.surfBuf)
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.surfBuf, (0, 0), self.screenrect)
        pygame.display.flip()
class errorHandler(chameleon.listener):
    def __init__(self, manager):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("serverError", self.ev_serverError)
        self.manager.reg("serverError", self)
    def ev_serverError(self, data):
        print "ERROR"
        self.manager.alert(chameleon.event("logout", None))
        raise errors.serverError(data)
class spinner(chameleon.manager):
    def __init__(self):
        chameleon.manager.__init__(self)
        self.errHandler = errorHandler(self)
        self.socket = socket.socket()
        self.socket.connect((CONFIG["host"], CONFIG["port"]))
        self.server = serverWrapper(self.socket)
        self.netView = networkView(self, self.server)
        self.netControl = networkController(self, self.server)
        self.keyControl = keyController(self)
        self.localView = localStateView(self)
    def main(self):
        clock = pygame.time.Clock()
        while 1:
            clock.tick(40)
            self.alert(chameleon.event("update", None))
evMan = spinner()
def run():
    evMan.main()
