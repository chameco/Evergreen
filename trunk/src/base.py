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
from OpenGL import GL
import chameleon
import pygame
import sys
import cPickle as pickle
@utils.serializable
class drawnObject(pygame.sprite.Sprite):
    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self)
        #print coords
        self.image = None
        self.rect = pygame.rect.Rect(coords, (32, 32))
        self.data = {}
    def draw(self, scale = 1):
        texwidth = self.image.width * scale
        texheight = self.image.height * scale

        originx = texwidth / 2
        originy = texheight / 2

        GL.glPushMatrix()
        GL.glTranslatef(self.rect.x, self.rect.y, 0)

        #glColor4f(color.r, color.g, color.b, color.a)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.image.surface)

        GL.glBegin(GL.GL_TRIANGLE_STRIP)
        GL.glTexCoord2f(0, self.image.height_ratio); GL.glVertex2f(-originx, texheight - originy)
        GL.glTexCoord2f(self.image.width_ratio, self.image.height_ratio); GL.glVertex2f(texwidth - originx, texheight - originy)
        GL.glTexCoord2f(0, 1); GL.glVertex2f(-originx, -originy)
        GL.glTexCoord2f(self.image.width_ratio, 1); GL.glVertex2f(texwidth - originx, -originy)
        GL.glEnd()
		
        GL.glPopMatrix()
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
class floor(drawnObject):
    def __init__(self, coords):
        drawnObject.__init__(self, coords)
class woodFloor(floor):
    def __init__(self, coords):
        floor.__init__(self, coords)
        self.imgname = "woodFloor"
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
class stairsWarp(block):
    def __init__(self, coords, warp):
        block.__init__(self, coords)
        print "stairswarpinit"
        self.warp = warp
        self.imgname = "warp"
    def hit(self, hitter):
        print "stairswarp"
        hitter.curLevel = self.warp
        print hitter
        hitter.manager.alert(chameleon.event("switchLevel", hitter))
class entity(physicalObject): #On the character creation webpage we'll need to add some additional attributes, such as name.
    amountCreated = 0
    def __init__(self, coords, data=None, manager=None, curLevel=0): #0 is north, 1 is south, 3 is west, 4 is east
        physicalObject.__init__(self, coords)
        if data is None:
            data = {"facing" : 0, "name" : self.__class__.__name__ + str(self.__class__.amountCreated)}
        self.__class__.amountCreated += 1
        self.data = data
        if manager:
            self.manager = manager
        self.curLevel = curLevel
        self.requestx = 0
        self.requesty = 0
        self.attrs = {"speed" : 8, "attack" : 1} #data is replicated, attrs are serverside. SPEED MUST BE A FACTOR OF BLOCK SIZE!
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
            collider = pygame.rect.Rect(self.rect.left + 8, self.rect.top - 16, 16, 16)
        elif self.data["facing"] == 1:
            collider = pygame.rect.Rect(self.rect.left + 8, self.rect.bottom + 16, 16, 16)
        elif self.data["facing"] == 2:
            collider = pygame.rect.Rect(self.rect.left - 16, self.rect.top + 8, 16, 16)
        elif self.data["facing"] == 3:
            collider = pygame.rect.Rect(self.rect.right + 16, self.rect.top + 8, 16, 16)
        sl = collider.collidelistall(allSprites)
        for index in sl:
            allSprites[index].hit(self)
    def update(self, allSprites):
        requestx = self.requestx
        requesty = self.requesty
        temp = [sprite for sprite in allSprites if sprite is not self]
        x = self.rect.move(requestx, 0).collidelist(temp)
        if x != -1:
            requestx = 0
        y = self.rect.move(0, requesty).collidelist(temp)
        if y != -1:
            requesty = 0
        self.rect.move_ip(requestx, requesty)
        if self.requestx or self.requesty:
            self.manager.alert(chameleon.event("entityMoved", (self, (self.rect.x, self.rect.y), self.curLevel)))
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
