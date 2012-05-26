from .... import base
class pitwall(base.block):
    def __init__(self, coords):
        base.block.__init__(self, coords)
        self.imgname = "pitwall"
class pitcreature(base.entity):
    def __init__(self, coords, data=None):#We might as well expose health, for health bars and stuff.
        if data is None:
            data = {"facing" : 0}
        base.entity.__init__(self, coords, data)
        self.wasjusthit = 0
        self.prev = 0
    def update(self, allSprites):
        if self.wasjusthit == 2:
            self.prev = self.data["facing"]
            self.data["facing"] = 4
            self.wasjusthit = 1
        elif self.wasjusthit == 1:
            self.data["facing"] = self.prev
            self.wasjusthit = 0
        if self.data["health"] <= 0:
            self.kill()
    def hit(self, hitter):
        print "hit"
        self.wasjusthit = 2
        self.data["health"] -= self.attrs["attack"]
class pittooth(pitcreature):
    def __init__(self, rect, data=None):
        if data is None:
            data = {"facing" : 0, "name" : "pittooth", "health" : 5}
        pitcreature.__init__(self, rect, data)
        self.imgname = "pittooth"
