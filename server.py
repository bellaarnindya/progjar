<<<<<<< HEAD
import socket
import select
import sys
import threading
import os


data = [{'u':'sabila', 'p': 'rani'}, {'u':'mila', 'p':'raras'}]
flag = 0
class Server:
	def __init__(self):
		self.host = 'localhost'
		self.port = 21
		self.backlog = 5
		self.size = 1024
		self.server = None
		self.threads = []

	def open_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))
		self.server.listen(5)
	def run(self):
		self.open_socket()
		inp = [self.server]
		running = 1
		while running:
			inputready, outputready, exceptready = select.select(inp,[],[])
			for s in inputready:
				if s == self.server:
					c = Client(self.server.accept())
					c.start()
					self.threads.append(c)

				elif s==sys.stdin:
					junk = sys.stdin.readline()
					running = 0

		self.server.close()
		for c in self.threads:
			c.join()
		sys.exit(0)

class Client(threading.Thread):
	def __init__(self,(client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.size = 1024

	def run(self):
		running = 1
		path = "E:/SABILA/Kuliah/SEMESTER 5/PROGJAR/fp"
		while running:
			command = self.client.recv(self.size)
			print 'recv: ', self.address, command
			if command:
				if "USER" in command:
					username = command.strip().split(' ')[1]
					response = "331 Password required for "+username
					self.client.send(response)
				elif "PASS" in command:
					password = command.strip().split(' ')[1]
					i=0
					while i<len(data):
						if (data[i]['u'] == username and data[i]['p']==password):
							response = "230 Logged on\r\n"
							os.chdir(path+"/"+username)
							path = path+"/"+username
							flag = 1
							break
						else:
							response = "530 Login or password incorrect!"
						i+=1
					self.client.send(response)
				elif "CWD" in command:
					if(flag == 1):
						cdir = command.strip().split('CWD ')[1]
						if (os.path.isdir(path+"/"+cdir)):
							os.chdir(path+"/"+cdir)
							response = "250 CWD successful. "+cdir+" is current directory."
						else:
							response = "550 CWD failed. "+cdir+": directory not found."
					else:
						response = "530 Please log in with USER and PASS first."
					self.client.send(response)
			else:
				self.client.close()
				running = 0
		

if __name__ == "__main__":
	s = Server()
	s.run()



import socket
import select
import sys
import threading
import os


data = [{'u':'sabila', 'p': 'rani'}, {'u':'mila', 'p':'raras'}]
flag = 0
class Server:
	def __init__(self):
		self.host = 'localhost'
		self.port = 21
		self.backlog = 5
		self.size = 1024
		self.server = None
		self.threads = []

	def open_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))
		self.server.listen(5)
	def run(self):
		self.open_socket()
		inp = [self.server]
		running = 1
		while running:
			inputready, outputready, exceptready = select.select(inp,[],[])
			for s in inputready:
				if s == self.server:
					c = Client(self.server.accept())
					c.start()
					self.threads.append(c)

				elif s==sys.stdin:
					junk = sys.stdin.readline()
					running = 0

		self.server.close()
		for c in self.threads:
			c.join()
		sys.exit(0)

class Client(threading.Thread):
	def __init__(self,(client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.size = 1024

	def run(self):
		running = 1
		path = "E:/SABILA/Kuliah/SEMESTER 5/PROGJAR/fp"
		while running:
			command = self.client.recv(self.size)
			print 'recv: ', self.address, command
			if command:
				if "USER" in command:
					username = command.strip().split(' ')[1]
					response = "331 Password required for "+username
					self.client.send(response)
				elif "PASS" in command:
					password = command.strip().split(' ')[1]
					i=0
					while i<len(data):
						if (data[i]['u'] == username and data[i]['p']==password):
							response = "230 Logged on\r\n"
							os.chdir(path+"/"+username)
							path = path+"/"+username
							flag = 1
							break
						else:
							response = "530 Login or password incorrect!"
						i+=1
					self.client.send(response)
				elif "CWD" in command:
					if(flag == 1):
						cdir = command.strip().split('CWD ')[1]
						if (os.path.isdir(path+"/"+cdir)):
							os.chdir(path+"/"+cdir)
							response = "250 CWD successful. "+cdir+" is current directory."
						else:
							response = "550 CWD failed. "+cdir+": directory not found."
					else:
						response = "530 Please log in with USER and PASS first."
					self.client.send(response)
			else:
				self.client.close()
				running = 0
		

if __name__ == "__main__":
	s = Server()
	s.run()
=======
import socket
import select
import sys
import threading


data = [{'u':'sabila', 'p': 'rani'}, {'u':'mila', 'p':'raras'}]
flag = 0

class Server:
	def __init__(self):
		self.host = 'localhost'
		self.port = 21
		self.backlog = 5
		self.size = 1024
		self.server = None
		self.threads = []

	def open_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))
		self.server.listen(5)

	def run(self):
		self.open_socket()
		inp = [self.server]
		running = 1
		while running:
			inputready, outputready, exceptready = select.select(inp,[],[])

			for s in inputready:
				if s == self.server:
					c = Client(self.server.accept())
					c.start()
					self.threads.append(c)

				elif s==sys.stdin:
					junk = sys.stdin.readline()
					running = 0

		self.server.close()
		for c in self.threads:
			c.join()
		sys.exit(0)

class Client(threading.Thread):
	def __init__(self,(client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.size = 1024

	def run(self):
		running = 1
		while running:
			command = self.client.recv(self.size)
			print 'recv: ', self.address, command
			if command:
				if "USER" in command:
					username = command.strip().split(' ')[1]
					response = "331 Password required for "+username+"\r\n"
					self.client.send(response)
				elif "PASS" in command:
					password = command.strip().split(' ')[1]
					i=0
					while i<len(data):
						if (data[i]['u'] == username and data[i]['p']==password):
							response = "230 Logged on\r\n"
							flag = 1
							break
						else:
							response = "530 Login or password incorrect!\r\n"
							#os.chdir("/"+username)	
						i+=1
					self.client.send(response)
				elif "CWD" in command:
					if(flag == 1):
						cdir = command.strip().split('CWD ')[1]
						path = "E:/SABILA/Kuliah/SEMESTER 5/PROGJAR/fp/progjar"
						#directory = os.chdir(path+"/"+cdir)
						#if(os.chdir("/"+cdir))

					else:
						response = "530 Please log in with USER and PASS first.\r\n"
					self.client.send(response)
			else:
				self.client.close()
				running = 0
	def QUIT(self,command):
		self.client.send('221 Goodbye.\r\n')
		running = False
		self.client.close()

if __name__ == "__main__":
	s = Server()
	s.run()
>>>>>>> a031b2b349c2747d095c39c7bd9444d2201a19b5
