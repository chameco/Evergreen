from ... import base
from ... import utils
from ... import level
from ... import errors
from ... import chameleon
class entityupdatemanager(chameleon.listener):
	def __init__(self, manager, controlledEntity):
		chameleon.listener.__init__(self)
		self.manager = manager
