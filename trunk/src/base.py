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
        print "physicalObject hit, self is:"
        print self
        pass
    def bump(self, bumper):
        print "bump"
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
    def __init__(self, coords, data=None, manager=None, curLevel=0):
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
        bumped = []
        x = self.rect.move(requestx, 0).collidelistall(temp)
        if len(x):
            requestx = 0
            bumped.extend(x)
        y = self.rect.move(0, requesty).collidelistall(temp)
        if len(y):
            requesty = 0
            bumped.extend(y)
        self.rect.move_ip(requestx, requesty)
        if self.requestx or self.requesty:
            self.manager.alert(chameleon.event("entityMoved", (self, (self.rect.x, self.rect.y), self.curLevel)))
        for index in bumped:
            allSprites[index].bump(self)
class player(entity):
    def __init__(self, coords, data=None, manager=None, curLevel=0):
        entity.__init__(self, coords, data, manager, curLevel)
        self.data["health"] = 10
        self.wasjusthit = 0
        self.prev = 0
    def update(self, allSprites):
        entity.update(self, allSprites)
        if self.wasjusthit == 2:
            self.prev = self.data["facing"]
            self.data["facing"] = 4
            self.wasjusthit = 1
            self.manager.alert(chameleon.event("entityMoved", (self, (self.rect.x, self.rect.y), self.curLevel)))
        elif self.wasjusthit == 1:
            self.data["facing"] = self.prev
            self.wasjusthit = 0
            self.manager.alert(chameleon.event("entityMoved", (self, (self.rect.x, self.rect.y), self.curLevel)))
        if self.data["health"] <= 0:
            self.manager.alert(chameleon.event("killEntity", self))
            self.kill()
            self.manager.alert(chameleon.event("gameOver", self))
    def hit(self, hitter):
        print "player hit"
        self.wasjusthit = 2
        self.data["health"] -= hitter.attrs["attack"]
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
