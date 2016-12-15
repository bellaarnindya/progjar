import socket
import select
import sys
import threading

class Server:
	def __init__(self):
		self.host = 'localhost'
		self.port = 21
		self.size = 1024
		self.threads = []

	def open_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))
		self.server.listen(5)

	def run(self):
		self.open_socket()
		input = [self.server, sys.stdin]
		running = 1
		while running:
			inputready, outputready, exceptready = select.select(input,[],[])

			for s in inputready:
				if s == self.server:
					c = Client(self.server.accept())
					c.start()
					self.threads.append(c)

				elif s==sys.stdin:
					command = sys.stdin.readline()
					running = 0

		self.server.close()
		for c in self.threads:
			c.join()

class Client(threading.Thread):
	def __init__(self,(client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.size = 1024

	def run(self):
		running = 1
		while running:
			data = self.client.recv(self.size)
			print 'recv: ', self.address, data
			if data:
				self.client.send(data)
			else:
				self.client.close()
				running = 0

if __name__ == "__main__":
	s = Server()
	s.run()