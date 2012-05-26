#!/usr/bin/python
import spritepacks.default as spritepack# This should eventually be loaded conditionally based on a config file.
from .. import base
from .. import level
from .. import errors
from .. import net
from .. import chameleon
import os
import sys
import socket
import collections
import pygame
import cPickle as pickle
import re
import select
pygame.init()
#pygame.display.set_mode((0, 0), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_mode()
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
class serverWrapper():
    def __init__(self, serversocket):
        self.socket = serversocket
        self.poll = select.poll()
        self.poll.register(self.socket, select.POLLIN)
        self.socket.send(sys.argv[3])
        ack = self.socket.recv(6)
        if ack != "idAck":
            raise errors.serverError("Error: server refuses to acknowledge ID message.")
    def postEvent(self, event, data):
        #print event
        #print data
        self.socket.send(pickle.dumps(net.netEvent(event, data)), 2)
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
        self.setResponse("initialStateReceived", self.ev_initialStateReceived)
        self.setResponse("entityPosReceived", self.ev_entityPosReceived)
        self.setResponse("update", self.ev_update)
        self.manager.reg("initialStateReceived", self)
        self.manager.reg("entityPosReceived", self)
        self.manager.reg("update", self)
        self.server = server
        self.blockState = None
        self.entityState = None
    def ev_initialStateReceived(self, data):
        print "Initial State Recieved"
        self.blockState = base.copyableGroup.load(data)
        self.manager.alert(chameleon.event("distState", self.blockState))# We do it this way so everyone has the same reference to the newly-loaded state. Probably unnessesary, but I like it.
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
        self.setResponse("distState", self.ev_distState)
        self.setResponse("distEntityPos", self.ev_distEntityPos)
        self.setResponse("update", self.ev_update)
        self.manager.reg("distState", self)
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
    def ev_distState(self, data):
        if self.blockState:
            self.blockState.clear()
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
        self.char = [char for char in self.entityState.sprites() if char.data["name"] == sys.argv[3]][0]
        #self.entityState.remove(self.char)
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
        self.socket.connect((sys.argv[1], int(sys.argv[2])))
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
