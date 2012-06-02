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
from . import utils
from . import errors
import chameleon
import pygame
pygame.init()
import sys
import cPickle as pickle
@utils.serializable
class drawnObject(pygame.sprite.Sprite):
    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self)
        #print coords
        self.image = None
        self.rect = pygame.rect.Rect(coords, (50, 50))
        self.data = {}
    def serialize(self):
        return {"type" : self.__class__, "coords" : (self.rect.x, self.rect.y), "data" : self.data}
    @staticmethod
    def load(dump, manager=None):
        data = dump
        #print data["coords"]
        #print data
        if "data" in data and data["data"]: #If data is set to a true value in the constructor, you better have an argument slot for it!
            if manager:
                return data["type"](data["coords"], data["data"], manager)
            else:
                return data["type"](data["coords"], data["data"])
        else:
            if manager:
                return data["type"](data["coords"], manager)
            else:
                return data["type"](data["coords"])
class physicalObject(drawnObject): #Abstract Base Class
    def __init__(self, coords):
        drawnObject.__init__(self, coords)
    def hit(self, hitter):
        print "hit"
        pass
class block(physicalObject): #Abstract Base Class
    def __init__(self, coords):
        physicalObject.__init__(self, coords)
class stone(block):
    def __init__(self, coords):
        block.__init__(self, coords)
        self.imgname = "stone"
class stairsUp(block):
    def __init__(self, coords):
        block.__init__(self, coords)
        print "stairsupinit"
        self.imgname = "up"
    def hit(self, hitter):
        print "stairsup"
        print "curLevel: " + str(hitter.curLevel)
        hitter.curLevel -= 1
        print hitter
        hitter.manager.alert(chameleon.event("switchLevel", hitter))
class stairsDown(block):
    def __init__(self, coords):
        block.__init__(self, coords)
        print "stairsdowninit"
        self.imgname = "down"
    def hit(self, hitter):
        print "stairsdown"
        hitter.curLevel += 1
        print hitter
        hitter.manager.alert(chameleon.event("switchLevel", hitter))
class entity(physicalObject): #On the character creation webpage we'll need to add some additional attributes, such as name.
    def __init__(self, coords, data=None, manager=None): #0 is north, 1 is south, 3 is west, 4 is east
        physicalObject.__init__(self, coords)
        if data is None:
            data = {"facing" : 0}
        self.data = data
        if manager:
            self.manager = manager
        self.curLevel = 0
        self.requestx = 0
        self.requesty = 0
        self.attrs = {"speed" : 10, "attack" : 1} #data is replicated, attrs are serverside. SPEED MUST BE A FACTOR OF 50!
        self.imgname = "entity" #Just for testing
    def moveup(self, down):
        #print "up"
        if down:
            self.data["facing"] = 0
            self.requesty = -(self.attrs["speed"])
        else:
            self.requesty = 0 if self.requesty <= -1 else self.requesty
    def movedown(self, down):
        #print "down"
        if down:
            self.data["facing"] = 1
            self.requesty = self.attrs["speed"]
        else:
            self.requesty = 0 if self.requesty >= 1 else self.requesty
    def moveleft(self, down):
        #print "left"
        if down:
            self.data["facing"] = 2
            self.requestx = -(self.attrs["speed"])
        else:
            self.requestx = 0 if self.requestx <= -1 else self.requestx
    def moveright(self, down):
        #print "right"
        if down:
            self.data["facing"] = 3
            self.requestx = self.attrs["speed"]
        else:
            self.requestx = 0 if self.requestx >= 1 else self.requestx
    def attack(self, allSprites):
        if self.data["facing"] == 0:
            collider = pygame.rect.Rect(self.rect.left + 15, self.rect.top - 25, 20, 20)
        elif self.data["facing"] == 1:
            collider = pygame.rect.Rect(self.rect.left + 15, self.rect.bottom + 5, 20, 20)
        elif self.data["facing"] == 2:
            collider = pygame.rect.Rect(self.rect.left - 25, self.rect.top + 15, 20, 20)
        elif self.data["facing"] == 3:
            collider = pygame.rect.Rect(self.rect.right + 5, self.rect.top + 15, 20, 20)
        sl = collider.collidelistall(allSprites)
        for index in sl:
            allSprites[index].hit(self)
    def update(self, allSprites):
        #print self.rect
        requestx = self.requestx
        requesty = self.requesty
        temp = [sprite for sprite in allSprites if sprite is not self]
        x = self.rect.move(requestx, 0).collidelist(temp)
        if x != -1:
            requestx = 0
        y = self.rect.move(0, requesty).collidelist(temp)
        if y != -1:
            requesty = 0
        #both = self.rect.move(requestx, requesty).collidelist(temp)#This stops the weird diagonal corners thingy.
        #if both != -1:
        #    requesty = requestx = 0
        self.rect.move_ip(requestx, requesty)
        #print self.rect
        #~ if self.health <= 0:
            #~ self.kill()
@utils.serializable
class copyableGroup(pygame.sprite.Group):
    def serialize(self):
        r = []
        for sprite in self:
            r.append(sprite.serialize())
        #print r
        return r
    @staticmethod
    def load(dump):
        r = copyableGroup()
        dsprites = dump
        for dsprite in dsprites:
            r.add(drawnObject.load(dsprite))
        return r
