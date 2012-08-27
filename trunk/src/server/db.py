from .. import base
from .. import errors
from .. import chameleon
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

