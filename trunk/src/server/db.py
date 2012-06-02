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
from .. import base
from .. import errors
import sqlite3
import atexit
import cPickle as pickle
class entityDBWrapper():
    def __init__(self, name):
        self.entityDB = sqlite3.connect(name)
        pass
    def fetchEntity(self, avatarID, manager):
        #return base.entity((100, 100), data={"facing" : 0, "name" : "chameco"})
        cur = self.entityDB.cursor()
        for entity in cur.execute("select data from chars where name=?", (avatarID,)):
            print entity
            t = pickle.loads(entity[0].encode("ascii"))
            return base.drawnObject.load(t, manager)# We only need the first match, there should only be one anyway.
        raise errors.dbError("Unknown avatar")
    def saveEntity(self, entity):
        cur = self.entityDB.cursor()
        cur.execute("update chars set data=? where name=?", (pickle.dumps(entity.serialize()), entity.data["name"]))
        self.entityDB.commit()
