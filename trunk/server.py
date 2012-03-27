import chameleon
import shelve
from twisted.spread import pb
from twisted.spread.pb import DeadReferenceError
from twisted.cred import checkers, portal
from zope.interface import implements
from pprint import pprint
import atexit
import base
pb.setUnjellyableForClassTree(base, base.drawnObject)
pb.setUnjellyableForClass(base.copyableGroup, base.copyableGroup)
entityDB = shelve.open("entity.db", protocol=2, writeback=True)
atexit.register(entityDB.close)
curGameState = base.copyableGroup()
def fetchEntity(avatarID):
	if not entityDB.has_key(avatarID):
		entityDB[avatarID] = base.entity(0)
	return entityDB[avatarID]
class RegularAvatar(pb.IPerspective): pass
class Realm(chameleon.listener):
	implements(portal.IRealm)
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("clientDisconnect", self.ev_clientDisconnect)
		self.manager.reg("clientDisconnect", self)
		# keep track of avatars that have been given out
		self.claimedAvatarIDs = []
		# we need to hold onto views so they don't get garbage collected
		self.clientViews = []
		# maps avatars to player(s) they control
		self.playersControlledByAvatar = {}
	def requestAvatar(self, avatarID, mind, *interfaces):
		print ' v'*30
		print 'requesting avatar id: ', avatarID
		print ' ^'*30
		if pb.IPerspective not in interfaces:
			print 'TWISTED FAILURE'
			raise NotImplementedError
		avatarClass = RegularAvatar
		if avatarID in self.claimedAvatarIDs:
			#avatarClass = DisallowedAvatar
			raise Exception( 'Another client is already connected'
							 ' to this avatar (%s)' % avatarID )

		self.claimedAvatarIDs.append(avatarID)

		# TODO: this should be ok when avatarID is checkers.ANONYMOUS
		if avatarID not in self.playersControlledByAvatar:
			self.playersControlledByAvatar[avatarID] = []
		view = networkView(self.manager, avatarID, mind)
		controller = networkController(self.manager, avatarID, self)
		self.clientViews.append(view)
		self.manager.alert(chameleon.event("clientConnect", fetchEntity(self.avatarID)))
		return avatarClass, controller, controller.clientDisconnect
	def knownPlayers(self):
		allPlayers = []
		for pList in self.playersControlledByAvatar.values():
			allPlayers.extend(pList)
		return allPlayers
	def ev_clientDisconnect(self, data):
		print 'got cli disconnect'
		self.claimedAvatarIDs.remove(data)
		removee = None
		for view in self.clientViews:
			if view.avatarID == data:
				removee = view
		if removee:
			self.clientViews.remove(removee)
		print 'after disconnect, state is:'
		pprint (self.__dict__)
class networkView(chameleon.listener):
	def __init__(self, manager, avatarID, client):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("clientConnect", self.ev_clientConnect)
		self.setResponse("kill", self.ev_kill)
		self.manager.reg("clientConnect", self)
		self.manager.reg("kill", self)
		self.avatarID = avatarID
		self.client = client
		self.controlledEntity = None
	def ev_clientConnect(self, data):
		self.controlledEntity = data
		self.client.callRemote("postEvent", "initialStateReceived", (curGameState, self.controlledEntity))
	def ev_kill(self):
		self.manager.unregister("clientConnect", self)
		self.manager.unregister("kill", self)
class networkController(chameleon.listener, pb.Avatar):
	def __init__(self, manager, avatarID, realm):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("clientConnect", self.ev_clientConnect)
		self.manager.reg("clientConnect", self)
		self.avatarID = avatarID
		self.realm = realm
		self.controlledEntity = None
	def ev_clientConnect(self, data):
		self.controlledEntity = data
	def clientDisconnect(self):
		self.manager.alert(chameleon.event("clientDisconnect", self.avatarID))
	def perspective_postEvent(self, name, data):
		event = chameleon.event(name, data)
		event.name = str(self.avatarID) + event.name
		self.manager.alert(event)
	def perspective_moveUp(self, down):
		self.controlledEntity.moveup(down)
	def perspective_moveDown(self, down):
		self.controlledEntity.movedown(down)
	def perspective_moveLeft(self, down):
		self.controlledEntity.moveleft(down)
	def perspective_moveRight(self, down):
		self.controlledEntity.moveright(down)
class spinner(chameleon.manager):
	def __init__(self):
		chameleon.manager.__init__(self)
		from twisted.internet import reactor
		realm = Realm(self)
		portl = portal.Portal(realm)
		checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(user1='pass1', user2='pass1')
		portl.registerChecker(checker)
		reactor.listenTCP(33333, pb.PBServerFactory(portl))
		reactor.run()
manager = spinner()
