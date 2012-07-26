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
from .... import base
import chameleon
class pitwall(base.block):
    def __init__(self, coords):
        base.block.__init__(self, coords)
        self.imgname = "pitwall"
class pitcreature(base.entity):
    def __init__(self, coords, data=None, manager=None, curLevel=0):
        base.entity.__init__(self, coords, data, manager, curLevel)
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
        print "hit"
        self.wasjusthit = 2
        self.data["health"] -= self.attrs["attack"]
class pittooth(pitcreature):
    def __init__(self, rect, data=None, manager=None, curLevel=0):
        pitcreature.__init__(self, rect, data, manager, curLevel)
        self.data["health"] = 5
        self.imgname = "pittooth"
