from . import chameleon
from . import base
from . import utils
import cPickle as pickle
import time
import pygame
pygame.init()
class levelManager(chameleon.listener):
    def __init__(self, manager):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("update", self.ev_update)
        self.setResponse("getLevel", self.ev_getLevel)
        self.setResponse("spawnEntity", self.ev_spawnEntity)
        self.manager.reg("update", self)
        self.manager.reg("getLevel", self)
        self.manager.reg("spawnEntity", self)
        self.curtime = time.time()
    #@utils.trace
    def ev_update(self, data):
        t = time.time()
        delta = t - self.curtime
        if delta >= 0.1:
            self.curtime = t
            for level in self.levels:
                t = list(level.blockState.sprites())#We need list to make a copy
                t.extend(level.entityState.sprites())
                level.entityState.update(t)
    #@utils.trace
    def ev_getLevel(self, data):
        self.manager.alert(chameleon.event("distLevel", (self.levels[data.curLevel], data.data["name"])))
    #@utils.trace
    def ev_spawnEntity(self, data):
        print "spawn entity"
        if data[0] not in self.levels[data[1]].entityState:
            print "entity spawned"
            self.levels[data[1]].entityState.add(data[0])
@utils.serializable
class level():
    def __init__(self):
        self.blocks =  {"#" : base.stone}
        self.blockState = base.copyableGroup()
        self.entityState = base.copyableGroup()
        self.startcoords = (0, 0)
        #loadLevel should be called in the constructor of derived classes
    def serialize(self):
        return {"type" : self.__class__, "blockState" : self.blockState.serialize(), "entityState" : self.entityState.serialize()}
    @staticmethod
    def load(dump, manager):
        data = dump
        r = data["type"]()
        r.blockState = base.copyableGroup.load(data["blockState"])
        r.entityState = base.copyableGroup.load(data["entityState"])
        return r
    def loadLevel(self):
        x = y = 0
        for c in self.levelimp:
            if c == "\n":
                y += 50
                x = 0
            elif c == "C":
                self.startcoords = (x, y)
                x += 50
            elif c == " ":
                x += 50
            else:
                if issubclass(self.blocks[c], base.entity):
                    self.entityState.add(self.blocks[c]((x, y)))
                else:
                    self.blockState.add(self.blocks[c]((x, y)))
                x += 50
