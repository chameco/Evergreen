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
#from .. import chameleon
import chameleon
import sqlite3
import atexit
import cPickle as pickle
class entityDBWrapper():
    def __init__(self, name, manager):
        self.entityDB = sqlite3.connect(name)
        self.manager = manager
    def fetchEntity(self, avatarID):
        cur = self.entityDB.cursor()
        for entity in cur.execute("select data from chars where name=?", (avatarID,)):
            print entity
            t = pickle.loads(entity[0].encode("ascii"))
            return base.drawnObject.load(t, self.manager)# We only need the first match, there should only be one anyway.
        raise errors.dbError("Unknown avatar")
    def saveEntity(self, entity):
        cur = self.entityDB.cursor()
        cur.execute("update chars set data=? where name=?", (pickle.dumps(entity.serialize()), entity.data["name"]))
        self.entityDB.commit()
class dbManager(chameleon.listener):
    def __init__(self, manager):
        chameleon.listener.__init__(self)
        self.manager = manager
        self.setResponse("fetchEntity", self.ev_fetchEntity)
        self.setResponse("saveEntity", self.ev_saveEntity)
        self.manager.reg("fetchEntity", self)
        self.manager.reg("saveEntity", self)
        self.db = entityDBWrapper("entity.db", self.manager)
    def ev_fetchEntity(self, data):
        print "distEntity_" + data
        self.manager.alert(chameleon.event("distEntity_" + data, self.db.fetchEntity(data)))
    def ev_saveEntity(self, data):
        self.db.saveEntity(data)

