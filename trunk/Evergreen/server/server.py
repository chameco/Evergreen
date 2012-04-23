from .. import base
from .. import utils
from .. import level
from .. import errors
from .. import chameleon
import db
import sys
import os
import atexit
import cPickle as pickle
import socket
import re
import ConfigParser
CONFIG = {}
CONFIG["basedir"] = os.path.abspath(".")
CONFIG["packagedir"] = os.path.join(CONFIG["basedir"], "Evergreen")
CONFIG["serverdir"] = os.path.join(CONFIG["packagedir"], "server")
configParser = ConfigParser.ConfigParser(CONFIG)
configParser.read(os.path.join(CONFIG["serverdir"], "server.ini"))
CONFIG["maxplayers"] = configParser.getint("core", "maxplayers")
CONFIG["port"] = configParser.getint("network", "port")
class clientWrapper():
	def __init__(self, clientsocket):
		self.socket = clientsocket
		self.avatarID = self.socket.recv(256)
		self.socket.send("idAck")
		self.buffer = ""
		self.requestRegex = re.compile("\\S+\\s\\S+\n")
	def postEvent(self, event, data):
		self.socket.send(event + " " + data + "\n")
	def getData(self):
		t = ""
		self.socket.recvinto(1024, t)
		t = t.split("\n")
		for request in t:
			if self.requestRegex.match(request) != None:
				self.buffer.append(request)
		return self.buffer[0]
	def bufLen(self):
		return len(self.buffer)
class networkSubsystem(chameleon.manager, chameleon.listener):
	"""networkSubsystem is a private manager class, one is instantiated for each client"""
	def __init__(self, manager, clientsocket):
		chameleon.manager.__init__(self)
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("update", self.ev_update)
		self.manager.reg("update", self)
		self.client = clientWrapper(clientsocket)
		try:
			self.controlledEntity = fetchEntity(self.client.avatarID)
		except errors.coreError as e:
			print "Unknown character"
			self.client.postEvent("serverError", "Unknown character")
			self.client.close()
			self.manager.unregister("update", self)
			self.manager.alert(chameleon.event("clientDisconnect", self))
		else:
			self.registerPlugin(networkView)
			self.registerPlugin(networkController)
	def registerPlugin(self, plugin, name):
		self.plugins[name] = plugin(self.manager, self.client, self.controlledEntity)
	def alertUp(self, event):
		self.manager.alert(event)
	def ev_update(self, data):
		self.alert(chameleon.event("update", None))
class networkView(chameleon.listener):
	def __init__(self, manager, client, controlledEntity):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("update", self.ev_update)
		self.manager.reg("update", self)
		self.client = client
		self.controlledEntity = controlledEntity
		self.client.postEvent("initialStateReceived", levelState[self.controlledEntity.curLevel].serialize())
		self.client.postEvent("controlledEntityReceived", self.controlledEntity.serialize())
		self.client.postEvent("entityPositionUpdate", entityState.serialize())
	def ev_update(self):
		self.client.postEvent("entityPositionUpdate", entityState.serialize())
class networkController(chameleon.listener):
	def __init__(self, manager, client, controlledEntity):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("update", self.ev_update)
		self.manager.reg("update", self)
		self.client = client
		self.controlledEntity = controlledEntity
	def ev_update(self, data):
		if self.client.lenBuf():
			try:
				data = self.client.getData()
				data = data.split(" ")
				self.manager.alert(data[0], data[1:])
			except KeyError:
				print self.client.postEvent("serverError", "Invalid Request: try updating client.")
class networkSubsystemDelegator(chameleon.listener):
	def __init__(self, manager):
		chameleon.listener.__init__(self)
		self.manager = manager
		self.setResponse("update", self.ev_update)
		self.setResponse("clientDisconnect", self.ev_clientDisconnect)
		self.manager.reg("update", self)
		self.manager.reg("clientDisconnect", self)
		self.netSubsystems = []
		self.socket = socket.socket()
		atexit.register(self.socket.close)
		self.socket.settimeout(0.01)
		self.socket.bind(("", CONFIG["port"]))
		self.socket.listen(5)
	def ev_update(self, data):
		if len(self.netSubsystems) <= CONFIG["maxplayers"]:
			try:
				client, addr = self.socket.accept()
				self.netSubsystems.append(networkSubsystem(self.manager, client))
			except socket.timeout:
				#print "Accept Timeout"
				pass
	def ev_clientDisconnect(self, data):
		self.netSubsystems.remove(data)
class spinner(chameleon.manager):
	def __init__(self):
		chameleon.manager.__init__(self)
		self.netSubDelegator = networkSubsystemDelegator(self)
	def main(self):
		while 1:
			self.alert(chameleon.event("update", None))
manager = spinner()
def run():
	"""We need this method to expose manager.main() to runserver.py in an appealing manner."""
	manager.main()
