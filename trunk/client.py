import chameleon
import sys
import pygame
import cPickle as pickle
from twisted.spread import pb
from twisted.internet import defer, reactor
from twisted.internet.task import LoopingCall
from twisted.cred import credentials
import base
pb.setUnjellyableForClassTree(base, base.drawnObject)
pb.setUnjellyableForClass(base.copyableGroup, base.copyableGroup)
pygame.init()
pygame.display.set_mode()
class networkController(chameleon.listener, pb.Root):
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("connectedToServer", self.ev_connectedToServer)
		self.setResponse("initialStateReceived", self.ev_initialStateReceived)
		self.setResponse("up", self.ev_up)
		self.setResponse("down", self.ev_down)
		self.setResponse("left", self.ev_left)
		self.setResponse("right", self.ev_right)
		self.manager.reg("connectedToServer", self)
		self.manager.reg("initialStateReceived", self)
		self.manager.reg("up", self)
		self.manager.reg("down", self)
		self.manager.reg("left", self)
		self.manager.reg("right", self)
		self.server = None
		self.state = None
	def remote_postEvent(self, name, data):
		self.manager.alert(chameleon.event(name, data))
	def ev_connectedToServer(self, data):
		self.server = data
		self.server.callRemote("postEvent", "clientConnect", False)
	def ev_initialStateReceived(self, data):
		print "Initial State Recieved"
		self.state = data[0]
		self.char = data[1]
		print self.state
	def ev_up(self, data):
		self.server.callRemote("moveUp", data)
	def ev_down(self, data):
		self.server.callRemote("moveDown", data)
	def ev_left(self, data):
		self.server.callRemote("moveLeft", data)
	def ev_right(self, data):
		self.server.callRemote("moveRight", data)
class networkView(chameleon.listener, pb.Referenceable):
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.pbClientFactory = pb.PBClientFactory()
		self.manager = manager
		self.setResponse("initialize", self.ev_initialize)
		self.setResponse("initialStateReceived", self.ev_initialStateReceived)
		self.setResponse("logout", self.ev_logout)
		self.manager.reg("initialize", self)
		self.manager.reg("initialStateReceived", self)
		self.manager.reg("logout", self)
		self.server = None
	def connected(self, data):
		self.server = data
		self.manager.alert(chameleon.event("connectedToServer", self.server))
	def ev_initialize(self, data):
		connection = reactor.connectTCP(data[1], int(data[2]), self.pbClientFactory)
		userCred = credentials.UsernamePassword(data[3], data[4])
		controller = networkController(self.manager)
		deferred = self.pbClientFactory.login(userCred, client=controller)
		deferred.addCallback(self.connected)
		reactor.run()
	def ev_initialStateReceived(self, data):
		self.state = data[0]
		self.char = data[1]
	def ev_logout(self, data):
		self.pbClientFactory.disconnect()
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
		self.setResponse("setDrawn", self.ev_setDrawn)
		self.setResponse("initialStateReceived", self.ev_initialStateRecieved)
		self.setResponse("update", self.ev_update)
		self.manager.reg("setDrawn", self)
		self.manager.reg("initialStateReceived", self)
		self.manager.reg("update", self)
		self.state = None
		self.char = None
		self.surfBuf = pygame.surface.Surface((5000, 5000)) #We can increase this later.
		self.screen = pygame.display.get_surface()
		self.screenrect = self.screen.get_rect()
	def ev_setDrawn(self, data):
		self.state.objects.add(data)
	def ev_initialStateRecieved(self, data):
		self.state = data[0]
		self.char = data[1]
	def ev_update(self, data):
		if self.state:
			self.screenrect.center = self.char.center
			self.state.objects.draw(self.surfBuf)
			self.screen.fill((0, 0, 0))
			self.screen.blit(self.surfBuf, (0, 0), self.screenrect)
			pygame.display.update()
class spinner(chameleon.manager):
	FPS = 40.0
	def __init__(self):
		chameleon.manager.__init__(self)
		netView = networkView(self)#Creates networkController
		keyControl = keyController(self)
		localView = localStateView(self)
		self.loopingCall = LoopingCall(self.alert, chameleon.event("update", False))
		interval = 1.0 / spinner.FPS
		self.loopingCall.start(interval)
		self.alert(chameleon.event("initialize", sys.argv))
	def stop(self):
		self.loopingCall.stop()
		exit(0)
evMan = spinner()
