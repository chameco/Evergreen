#!/usr/bin/python
from .. import base
from .. import level
from .. import errors
from .. import chameleon
import os
import sys
import pygame
import cPickle as pickle
import re
pygame.init()
pygame.display.set_mode()
def loadImage(pathname):
	i = pygame.image.load(os.path.join("data", pathname))
	i.convert()
	return i
spritesheet = loadImage("spritesheet.png")
images = {}
charimages = {}
def getCharImage(name):
	if name in charimages.keys():
		pass
	else:
		charimages[name] = ((loadImage("playerf.png"), loadImage("playerfa.png")), (loadImage("playerb.png"), loadImage("playerba.png")), (loadImage("playerl.png"), loadImage("playerla.png")), (loadImage("playerr.png"), loadImage("playerra.png")))
	return charimages[name]
class serverWrapper():
	def __init__(self, serversocket):
		self.socket = serversocket
		self.socket.send(sys.argv[3])
		ack = self.socket.recv(5)
		if ack != "idAck":
			raise errors.serverError("Error: server refuses to acknowledge ID message.")
		self.buffer = ""
		self.requestRegex = re.compile("\\S+\\s\\S+\n")
	def postEvent(self, event, data):
		self.socket.send(event + " " + data + "\n")
	def getData(self):
		t = ""
		self.socket.recvinto(1024, t)
		t = t.split("\n")
		for request in t:
			if self.requestRegex.match(request) != None:
				self.buffer.append(request)
		return self.buffer[0]
	def bufLen(self):
		return len(self.buffer)
class networkController(chameleon.listener):
	def __init__(self, manager, server):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("initialStateReceived", self.ev_initialStateReceived)
		self.setResponse("update", self.ev_update)
		self.manager.reg("initialStateReceived", self)
		self.manager.reg("update", self)
		self.server = server
		self.state = None
	def ev_initialStateReceived(self, data):
		print "Initial State Recieved"
		self.state = base.copyableGroup.load(data)
		print self.state.sprites()
		self.manager.alert(chameleon.event("distState", self.state)
	def ev_update(self, data):
		if self.server.bufLen():
			response = self.server.getData().split(" ")
			self.manager.alert(chameleon.event(response[0], response[1]))
class networkView(chameleon.listener):
	def __init__(self, manager, server):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("initialize", self.ev_initialize)
		self.setResponse("distState", self.ev_distState)
		self.setResponse("logout", self.ev_logout)
		self.setResponse("up", self.ev_up)
		self.setResponse("down", self.ev_down)
		self.setResponse("left", self.ev_left)
		self.setResponse("right", self.ev_right)
		self.manager.reg("initialize", self)
		self.manager.reg("distState", self)
		self.manager.reg("logout", self)
		self.manager.reg("up", self)
		self.manager.reg("down", self)
		self.manager.reg("left", self)
		self.manager.reg("right", self)
		self.server = server
	def ev_up(self, data):
		self.server.postEvent("moveUp", data)
	def ev_down(self, data):
		self.server.postEvent("moveDown", data)
	def ev_left(self, data):
		self.server.postEvent("moveLeft", data)
	def ev_right(self, data):
		self.server.postEvent("moveRight", data)
class keyController(chameleon.listener):
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("update", self.ev_update)
		self.manager.cleanreg("update", self)
	def quit(self):
		self.manager.alert(chameleon.event("logout", False))
		self.manager.stop()
	def ev_update(self, data):
		currentEvent = pygame.event.poll()
		if currentEvent.type == pygame.QUIT: 
			reactor.addSystemEventTrigger('after', 'shutdown', self.quit)
			reactor.stop()
		elif currentEvent.type == pygame.KEYDOWN:
			self.manager.alert(chameleon.event(pygame.key.name(currentEvent.key), True))
		elif currentEvent.type == pygame.KEYUP:
			self.manager.alert(chameleon.event(pygame.key.name(currentEvent.key), False))
class localStateView(chameleon.listener):
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("distState", self.ev_distState)
		self.setResponse("update", self.ev_update)
		self.manager.reg("distState", self)
		self.manager.reg("update", self)
		self.state = None
		self.char = None
		self.surfBuf = pygame.surface.Surface((5000, 5000)) #We can increase this later.
		self.screen = pygame.display.get_surface()
		self.screenrect = self.screen.get_rect()
		self.clearcallback = lambda surf, rect : surf.fill((0, 0, 0), rect)
	def ev_distState(self, data):
		self.state, self.char = data
		self.chargroup = pygame.sprite.GroupSingle(self.char)
		self.char.image = getCharImage(self.char.data["name"])[self.char.data["facing"]][0]
		for sprite in self.state.sprites():
			if sprite.spriteoffset in images.keys():
				pass
			else:
				images[sprite.spriteoffset] = pygame.surface.Surface((50, 50))
				images[sprite.spriteoffset].blit(spritesheet, (0, 0), (sprite.spriteoffset, 0, 50, 50))
			sprite.image = images[sprite.spriteoffset]
		self.state.draw(self.surfBuf)
	def ev_update(self, data):
		if self.state:
			self.screenrect.center = self.char.rect.center
			self.chargroup.clear(self.surfBuf, self.clearcallback)
			self.chargroup.draw(self.surfBuf)
			self.screen.fill((0, 0, 0))
			self.screen.blit(self.surfBuf, (0, 0), self.screenrect)
			pygame.display.update()
class errorHandler(chameleon.listener):
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.setResponse("serverError", self.ev_serverError)
		self.manager.reg("serverErrror", self)
	def ev_serverError(self, data):
		raise errors.serverError(data)
class spinner(chameleon.manager):
	def __init__(self):
		chameleon.manager.__init__(self)
		self.socket = socket.socket()
		self.socket.connect((sys.argv[1], sys.argv[2]))
		self.server = serverWrapper(self, self.socket)
		self.netView = networkView(self, self.server)
		self.netControl = networkController(self, self.server)
		self.keyControl = keyController(self)
		self.localView = localStateView(self)
		self.errHandler = errorHandler(self)
	def main(self):
		while 1:
			self.alert(chameleon.event("update", None))
evMan = spinner()
