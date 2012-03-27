import chameleon
import pygame
from twisted.spread import pb
pygame.init()
class copyableGroup(pb.Copyable, pb.RemoteCopy, pygame.sprite.Group):
	pass
class drawnObject(pb.Copyable, pb.RemoteCopy, pygame.sprite.Sprite):
	def __init__(self, spriteoffset):
		pygame.sprite.Sprite.__init__(self)
		self.spriteoffset = spriteoffset
		self.image = None
		self.rect = None
class physicalObject(drawnObject): #Abstract Base Class
	def __init__(self, spriteoffset):
		drawnObject.__init__(self, spriteoffset)
class block(physicalObject): #Abstract Base Class
	def __init__(self, spriteoffset):
		physicalObject.__init__(self)
class stone(block):
	def __init__(self):
		block.__init__(self, 0)
class entity(physicalObject): #Abstract Base Class
	def __init__(self, spriteoffset):
		physicalObject.__init__(self, spriteoffset)
		self.facing = "n"
		self.requestx = 0
		self.requesty = 0
		self.attrs = {"speed" : 10}
	def moveup(self, down):
		if down:
			self.facing = "n"
			self.requesty = -(self.attrs["speed"])
		else:
			self.requesty = 0 if self.requesty <= -1 else self.requesty
	def movedown(self, down):
		if down:
			self.facing = "s"
			self.requesty = self.attrs["speed"]
		else:
			self.requesty = 0 if self.requesty >= 1 else self.requesty
	def moveleft(self, down):
		if down:
			self.facing = "w"
			self.requestx = -(self.attrs["speed"])
		else:
			self.requestx = 0 if self.requestx <= -1 else self.requestx
	def moveright(self, down):
		if down:
			self.facing = "e"
			self.requestx = self.attrs["speed"]
		else:
			self.requestx = 0 if self.requestx >= 1 else self.requestx
