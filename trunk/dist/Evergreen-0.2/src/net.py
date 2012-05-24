from . import chameleon
#import multiprocessing
#import collections
#class FakePipe():
#	def __init__(self):
#		self.queue = collections.deque()
#		self.count = 0
#	def send(self, obj):
#		self.queue.append(obj)
#		self.count += 1
#	def recv(self):
#		self.count -= 1
#		return self.queue.popleft()
#	def poll(self):
#		return self.count
class netEvent():
	def __init__(self, event):
		self.name = event.name
		self.data = event.data
	def __init__(self, name, data):
		self.name = name
		self.data = data
	def cham(self):
		return chameleon.event(self.name, self.data)
#class netManager():
#	def __init__(self):
#		self.processes = []
#		self.listeners = {}
#	def makeListener(self, liscls, events):
#		conn1, conn2 = multiprocessing.Pipe()
#		for event in events:
#			self.reg(event, conn2)
#		self.processes.append((multiprocessing.Process(target=liscls, args=(conn1,)), conn2))
#	def reg(self, event, conn):
#		self.listeners[event] = conn
#	def alert(self, event):
#		self.listeners[event.name].send(event)
#	def main(self):
#		for proc, conn in self.processes:
#			proc.start()
#		while 1:
#			for proc, conn in self.processes:
#				if conn.poll():
#					self.alert(conn.recv())
#			self.alert(netEvent("update", None))
#class netListener(chameleon.listener):
#	def __init__(self, conn):
#		chameleon.listener.__init__(self)
#		self.manager = conn
#	def main(self):
#		while 1:
#			if self.manager.poll():
#				self.alert(self.manager.recv().cham())
#if __name__ == '__main__':
#	m = netManager()
#	class new(netListener):
#		def __init__(self, conn):
#			netListener.__init__(self, conn)
#			self.setResponse("update", self.ev_update)
#		def ev_update(self, data):
#			print "YO!"
#	m.makeListener(new, ["update"])
#	m.main()