from ... import base
from ... import utils
from ... import level
from ... import errors
from ... import chameleon
import copy
class movementmanager(chameleon.listener):
    def __init__(self, manager, controlledEntity):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.controlledEntity = controlledEntity
        self.setResponse("distLevel", self.ev_distLevel)
        self.manager.reg("distLevel", self)
        self.manager.alert(chameleon.event("getLevel", True))#Passing True stops the server from resending the block state.
    def ev_distLevel(self, data):
        self.level = data
        self.manager.unregister("distLevel", self)
        self.setResponse("up", self.ev_up)
        self.setResponse("down", self.ev_down)
        self.setResponse("left", self.ev_left)
        self.setResponse("right", self.ev_right)
        self.setResponse("attack", self.ev_attack)
        self.manager.reg("up", self)
        self.manager.reg("down", self)
        self.manager.reg("left", self)
        self.manager.reg("right", self)
        self.manager.reg("attack", self)
    def ev_up(self, data):
        #print "up"
        self.controlledEntity.moveup(data)
    def ev_down(self, data):
        #print "down"
        self.controlledEntity.movedown(data)
    def ev_left(self, data):
        #print "left"
        self.controlledEntity.moveleft(data)
    def ev_right(self, data):
        #print "right"
        self.controlledEntity.moveright(data)
    def ev_attack(self, data):
        #print "attack"
        if data:
            t = copy.copy(self.level.blockState.sprites())
            t.extend(self.level.entityState.sprites())
            self.controlledEntity.attack(t)
