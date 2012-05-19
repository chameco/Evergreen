from .. import base
from .. import errors
import sqlite3
import atexit
class entityDBWrapper():
	def __init__(self, name):
		self.entityDB = sqlite3.connect(name)
		pass
	def fetchEntity(self, avatarID):
		#return base.entity((100, 100), data={"facing" : 0, "name" : "chameco"})
		cur = self.entityDB.cursor()
		for entity in cur.execute("select data from chars where name=?", (avatarID,)):
			return base.drawnObject.load(pickle.loads(entity))# We only need the first match, there should only be one anyway.
		raise errors.dbError("Unknown avatar")
