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
CONFIG["font"] = configParser.get("video", "font")
PARSER = argparse.ArgumentParser(description="Launch the Evergreen client")
PARSER.add_argument("--playername", dest="playername", default=CONFIG["playername"], type=str, help="specify player name (overrides the configuration file)")
PARSER.add_argument("--port", dest="port", default=CONFIG["port"], type=int, help="specify server port (overrides the configuration file)")
PARSER.add_argument("--host", dest="host", default=CONFIG["host"], type=str, help="specify server address (overrides the configuration file)")
PARSER.add_argument("--fullscreen", dest="fullscreen", default=CONFIG["fullscreen"], type=int, help="specify whether or not to run in fullscreen (0 or 1, overrides the configuration file)")
PARSER.add_argument("--spritepack", dest="spritepack", default=CONFIG["spritepack"], type=str, help="specify spritepack to use (overrides the configuration file)")
PARSER.add_argument("--font", dest="font", default=CONFIG["font"], type=str, help="specify font to use (overrides the configuration file)")
ARGS = PARSER.parse_args()
CONFIG["playername"] = ARGS.playername
CONFIG["port"] = ARGS.port
CONFIG["host"] = ARGS.host
CONFIG["fullscreen"] = ARGS.fullscreen
CONFIG["spritepack"] = ARGS.spritepack
CONFIG["font"] = ARGS.font
from gloss import *
from .. import base
from .. import level
from .. import errors
from .. import utils
exec("import spritepacks." + CONFIG["spritepack"] + " as spritepack")
class serverWrapper():
    def __init__(self, serversocket):
        self.socket = serversocket
        self.poll = select.poll()
        self.poll.register(self.socket, select.POLLIN)
        self.socket.send(CONFIG["playername"])
    def postEvent(self, event, data):
        #print event
        #print data
        self.socket.send(pickle.dumps(utils.netEvent(event, data), 2))
    def getData(self):
        #print "getData"
        request = ""
        while self.poll.poll(0):
            request += self.socket.recv(8192)
            #print request
        if request != "":
            t = request.split("\xEE")#An unused delimiter character
            return [pickle.loads(x).cham() for x in t if len(x)]
        return None
    def close(self):
        self.socket.close()
class networkController(chameleon.listener):
    def __init__(self, manager, server):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("levelReceived", self.ev_levelReceived)
        self.setResponse("update", self.ev_update)
        self.manager.reg("levelReceived", self)
        self.manager.reg("update", self)
        self.server = server
        self.blockState = None
        self.floorState = None
        self.entityState = None
    def ev_levelReceived(self, data):
        print "Block State Received"
        print base
        self.blockState = base.copyableGroup.load(data[0])
        self.floorState = base.copyableGroup.load(data[1])
        self.entityState = base.copyableGroup.load(data[2])
        self.manager.alert(chameleon.event("distLevel", (self.blockState, self.floorState, self.entityState)))# We do it this way so everyone has the same reference to the newly-loaded state. Probably unnessesary, but I like it.
        self.server.postEvent("ackBlockState", None)
    def ev_update(self, data):
        responses = self.server.getData()
        #print response
        if responses:
            for response in responses:
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
class glGame(GlossGame, chameleon.manager, chameleon.listener):
    def __init__(self):
        GlossGame.__init__(self, "Evergreen")
        chameleon.manager.__init__(self)
        chameleon.listener.__init__(self)
        self.setResponse("distLevel", self.ev_distLevel)
        self.setResponse("entityMoved", self.ev_entityMoved)
        self.setResponse("entitySpawned", self.ev_entitySpawned)
        self.setResponse("entityKilled", self.ev_entityKilled)
        self.setResponse("gameOver", self.ev_gameOver)
        self.reg("distLevel", self)
        self.reg("entityMoved", self)
        self.reg("entitySpawned", self)
        self.reg("entityKilled", self)
        self.reg("gameOver", self)
        self.on_key_down = self.keydown
        self.on_key_up = self.keyup
        self.on_quit = self.quit
        self.blockState = []
        self.floorState = []
        self.entities = {}
    def ev_distLevel(self, data):
        print "diststate"
        Gloss.clear(Color.BLACK)
        self.blockState = []
        self.floorState = []
        self.entities = {}
        blockState = data[0]
        floorState = data[1]
        entityState = data[2]
        for sprite in blockState.sprites():
            sprite.image = spritepack.getImage(sprite.imgname)
            self.blockState.append(sprite)
        for sprite in floorState.sprites():
            sprite.image = spritepack.getImage(sprite.imgname)
            self.blockState.append(sprite)
        for sprite in entityState.sprites():
            sprite.images = spritepack.getEntityImage(sprite.imgname)
            sprite.image = sprite.images[sprite.data["facing"]][0]
            self.entities[sprite.data["name"]] = sprite
        self.drawSprites()
    def ev_entityMoved(self, data):
        sprite = base.drawnObject.load(data[0])
        if sprite.data["name"] in self.entities:
            sprite.images = spritepack.getEntityImage(sprite.imgname)
            sprite.image = sprite.images[sprite.data["facing"]][0]
            self.entities[sprite.data["name"]] = sprite
    def ev_entitySpawned(self, data):
        print "entitySpawned"
        sprite = base.drawnObject.load(data)
        sprite.images = spritepack.getEntityImage(sprite.imgname)
        sprite.image = sprite.images[sprite.data["facing"]][0]
        self.entities[sprite.data["name"]] = sprite
    def ev_entityKilled(self, data):
        print "entityKilled"
        sprite = base.drawnObject.load(data)
        del self.entities[sprite.data["name"]]
    def ev_gameOver(self, data):
        print "GAME OVER"
        Gloss.clear(Color.BLACK)
        self.loadingFont.draw(text="GAME OVER")
    def preload_content(self):
        self.loadingFont = SpriteFont(os.path.join("src", "client", "spritepacks", CONFIG["spritepack"], CONFIG["font"]))
    def draw_loading_screen(self):
        Gloss.clear(Color.BLACK)
        self.loadingFont.draw(text="loading...")
    def load_content(self):
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
        spritepack.loadImages()
        self.socket = socket.socket()
        self.socket.connect((CONFIG["host"], CONFIG["port"]))
        self.server = serverWrapper(self.socket)
        self.netView = networkView(self, self.server)
        self.netControl = networkController(self, self.server)
    def keydown(self, event):
        self.alert(chameleon.event(pygame.key.name(event.key), True))
    def keyup(self, event):
        self.alert(chameleon.event(pygame.key.name(event.key), False))
    def quit(self):
        self.alert(chameleon.event("logout", None))
    def draw(self):
        self.alert(chameleon.event("update", None))
        self.drawSprites()
    def drawSprites(self):
        if CONFIG["playername"] in self.entities:
            glTranslatef(Gloss.screen_resolution[0]/2 - self.entities[CONFIG["playername"]].rect.x, Gloss.screen_resolution[1]/2 - self.entities[CONFIG["playername"]].rect.y, 0)
            Gloss.clear(Color.BLACK)
            for block in self.blockState:
                block.draw() #Unneeded
            for floor in self.floorState:
                floor.draw()
            for entity in self.entities.values():
                entity.draw()
            glLoadIdentity();
evMan = glGame()
if CONFIG["fullscreen"]:
    Gloss.full_screen = True
def run():
    evMan.run()
