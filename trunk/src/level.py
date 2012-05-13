import chameleon
import pygame
pygame.init()
import base
import utils
import cPickle as pickle
@utils.serializable
class level(chameleon.listener):
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("getLevel", self.ev_getLevel)
		self.setResponse("getEntityState", self.ev_getEntityState)
		self.setResponse("spawnEntity", self.ev_spawnEntity)
		self.manager.reg("getLevel", self)
		self.manager.reg("getEntityState", self)
		self.manager.reg("spawnEntity", self)
		self.blocks =  {"#" : base.stone}
		self.allSprites = base.copyableGroup()
		self.entityState = base.copyableGroup()
		#loadLevel should be called in the constructor of derived classes
	def serialize(self):
		return {"type" : self.__class__, "allSprites" : self.allSprites.serialize(), "entityState" : self.entityState.serialize()}
	@staticmethod
	def load(dump, manager):
		data = dump
		r = data["type"](manager)
		r.allSprites = base.copyableGroup.load(data["allSprites"])
		r.entityState = base.copyableGroup.load(data["entityState"])
		return r
	def loadLevel(self):
		x = y = 0
		for c in self.levelimp:
			#~ if c == "<" or c == ">":
				#~ self.allSprites.add(self.blocks[c](rect.Rect(x, y, 50, 50), self.manager))
				#~ x += 50
			if c == "\n":#change back to elif later
				y += 50
				x = 0
			elif c == " ":
				x += 50
			else:
				self.allSprites.add(self.blocks[c]((x, y)))
				x += 50
	def ev_getLevel(self, data):
		self.manager.alert(chameleon.event("distLevel", self))
	def ev_getEntityState(self, data):
		#print "level.getEntityState"
		self.manager.alert(chameleon.event("distEntityState", self.entityState))
	def ev_spawnEntity(self, data):
		print "spawn entity"
		if data not in self.entityState:
			self.entityState.add(data)
