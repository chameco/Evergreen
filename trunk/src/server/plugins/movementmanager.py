from ... import base
from ... import utils
from ... import level
from ... import errors
from ... import chameleon
class movementmanager(chameleon.listener):
	def __init__(self, manager, controlledEntity):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.controlledEntity = controlledEntity
		self.setResponse("up", self.ev_up)
		self.setResponse("down", self.ev_down)
		self.setResponse("left", self.ev_left)
		self.setResponse("right", self.ev_right)
		self.manager.reg("up", self)
		self.manager.reg("down", self)
		self.manager.reg("left", self)
		self.manager.reg("right", self)
	def ev_up(self, data):
		print "up"
		self.controlledEntity.moveup(data)
	def ev_down(self, data):
		print "down"
		self.controlledEntity.movedown(data)
	def ev_left(self, data):
		print "left"
		self.controlledEntity.moveleft(data)
	def ev_right(self, data):
		print "right"
		self.controlledEntity.moveright(data)
