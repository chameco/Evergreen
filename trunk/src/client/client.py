import os
import sys
import socket
import collections
import pygame
import cPickle as pickle
import re
import select
from .. import chameleon
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
        self.socket.sendall(pickle.dumps(utils.netEvent(event, data), 2))
    def getData(self):
        #print "getData"
        request = ""
        p = self.poll.poll(0)
        while p:
            print p
            if p[0][1] == select.POLLIN:
                t = self.socket.recv(8192)
                if t:
                    request += t
                    p = self.poll.poll(0)
                else:
                    break
            else:
                break
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
        if responses:
            for response in responses:
                if response == "gameOver":
                    print "GAME OVER: ev_update"
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
class clientState():
    def __init__(self, game):
        pass
    def on_key_down(self, event): #self will be replaced by the instance of glGame
        pass
    def on_key_up(self, event):
        pass
    def on_quit(self, event):
        self.alert(chameleon.event("logout", None))
    def draw(self):
        pass
class drawState(clientState):
    def __init__(self, game):
        pygame.event.set_blocked([pygame.mousemotion, pygame.mousebuttonup, pygame.mousebuttondown])
        game.loadingFont = SpriteFont(os.path.join("src", "client", "spritepacks", CONFIG["spritepack"], CONFIG["font"]))
        spritepack.loadimages()
        game.socket = socket.socket()
        game.socket.connect((config["host"], config["port"]))
        game.server = serverwrapper(self.socket)
        game.netview = networkview(self, self.server)
        game.netControl = networkController(self, self.server)
    def on_key_down(self, event):
        self.alert(chameleon.event(pygame.key.name(event.key), True))
    def on_key_up(self, event):
        self.alert(chameleon.event(pygame.key.name(event.key), False))
    def draw(self):
        self.alert(chameleon.event("update", None))
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
class gameOverState(clientState):
    def draw(self):
        Gloss.clear(Color.BLACK)
        self.loadingFont.draw(text="GAME OVER")
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
        self.blockState = []
        self.floorState = []
        self.entities = {}
        self.loadState(drawState)
    def loadState(self, state):
        s = state(self)
        self.on_key_down = state.on_key_down
        self.on_key_up = state.on_key_up
        self.on_quit = state.on_quit
        self.draw = state.draw
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
        self.draw()
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
        self.state = "gameOver"
        self.on_key_down = utils.sponge
        self.on_key_up = utils.sponge
evMan = glGame()
if CONFIG["fullscreen"]:
    Gloss.full_screen = True
def run():
    evMan.run()
