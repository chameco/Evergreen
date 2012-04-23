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
		self.setResponse("getLevel", ev_getLevel)
		self.manager.cleanreg("getLevel", self)
		self.blocks =  {"#" : labyrinthStone,
						">" : StairsDown,
						"<" : StairsUp}
		self.allSprites = base.copyableGroup()
		#loadLevel should be called in the constructor of derived classes
	def serialize(self):
		return pickle.dumps({"type" : self.__class__.__name__, "allSprites" : self.allSprites.serialize()})
	@staticmethod
	def load(dump, manager):
		data = pickle.loads(dump)
		exec("mod = " + data["type"])
		r = mod(manager, levelManager)
		r.allSprites = data["allSprites"]
		return r
	def loadLevel(self):
		x = y = 0
		for c in self.levelimp:
			if c == "<" or c == ">":
				self.allSprites.add(self.blocks[c](rect.Rect(x, y, 50, 50), self.evman))
				x += 50
			elif c == "\n":
				y += 50
				x = 0
			elif c == " ":
				x += 50
			else:
				self.allSprites.add(self.blocks[c](rect.Rect(x, y, 50, 50)))
				x += 50
	def ev_getLevel(self):
		self.manager.alert(chameleon.event("distLevel", self))
