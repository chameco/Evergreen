from .... import base
from .... import chameleon
class pitwall(base.block):
    def __init__(self, coords, curLevel):
        base.block.__init__(self, coords, curLevel)
        self.imgname = "pitwall"
class pitcreature(base.entity):
    def __init__(self, coords, curLevel):
        base.entity.__init__(self, coords, curLevel)
        self.wasjusthit = 0
        self.prev = 0
    def update(self, allSprites):
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
    def hit(self, hitter):
        print "pit hit"
        self.wasjusthit = 2
        self.data["health"] -= hitter.attrs["attack"]
class pittooth(pitcreature):
    def __init__(self, coords, curLevel):
        pitcreature.__init__(self, coords, curLevel)
        self.data["health"] = 5
        self.imgname = "pittooth"
    def bump(self, bumper):
        bumper.hit(self)
