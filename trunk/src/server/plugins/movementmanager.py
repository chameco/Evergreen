#Copyright 2011 Samuel Breese. Distributed under the terms of the GNU General Public License.
#This file is part of Evergreen.
#
#    Evergreen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Evergreen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Evergreen.  If not, see <http://www.gnu.org/licenses/>.
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
        self.level = None
        self.controlledEntity = controlledEntity
        self.setResponse("distLevel", self.ev_distLevel)
        self.manager.reg("distLevel", self)
        self.manager.alert(chameleon.event("getLevel", None))#Passing True stops the server from resending the block state.
    def ev_distLevel(self, data):
        if not self.level:
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
        self.level = data
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
