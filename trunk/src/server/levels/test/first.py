from .... import level
from .... import base
import pygame
pygame.init()
class Scarecrow(base.entity):
    def __init__(self, rect, data={"facing" : 0, "name" : "scarecrow", "health" : 10}):#We might as well expose health, for health bars and stuff.
        base.entity.__init__(self, rect, data)
        self.imgname = "Scarecrow"
        self.wasjusthit = 0
        self.prev = 0
    def update(self, allSprites):
        if self.wasjusthit >= 2:
            self.prev = self.data["facing"]
            self.data["facing"] = 4
            self.wasjusthit = self.wasjusthit - 1
        elif self.wasjusthit == 1:
            self.data["facing"] = self.prev
            self.wasjusthit = 0
        if self.data["health"] <= 0:
            self.kill()
    def hit(self, hitter):
        self.wasjusthit = 2
        self.data["health"] -= self.attrs["attack"]
class lvl(level.level):
    def __init__(self, manager):
        level.level.__init__(self, manager)
        self.levelimp = """
##########
#        #
#        #
#        #
#        #
#        #
##########
"""
        self.loadLevel()
        self.entityState.add(Scarecrow((100, 100)))
