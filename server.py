import socket
import select
import sys
import threading
import os

#rani
#raras
data = [{'u':'sabila', 'p': 'rani'}, {'u':'mila', 'p':'raras'}]
flag = 0
src = ''
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
		base = "D:/Docs/ITS/Kuliah/Semester 5/PROGJAR/FP/progjar"
		while running:
			command = self.client.recv(self.size)
			print 'recv: ', self.address, command
			if command:
				if "USER" in command:
					username = command.strip().split(' ')[1]
					print username
					response = "331 Password required for "+username
					self.client.send(response)
				elif "PASS" in command:
					password = command.strip().split(' ')[1]
					print password
					i=0
					while i<len(data):
						if (data[i]['u'] == username and data[i]['p']==password):
							response = "230 Logged on\r\n"
							os.chdir(base+"/"+username)
							path = base+"/"+username
							flag = 1
							break
						else:
							response = "530 Login or password incorrect!"
							username = ''
						i+=1
					self.client.send(response)
				elif "CWD" in command:
					if(flag == 1):
						cdir = command.strip().split('CWD ')[1]
						if (os.path.isdir(path+"/"+cdir)):
							if ".." in cdir:
								os.chdir(base+"/"+username)
								response = "250 CWD successful. "+username+" is current directory."
							else:
								os.chdir(path+"/"+cdir)
								response = "250 CWD successful. "+cdir+" is current directory."
						else:
							response = "550 CWD failed. "+cdir+": directory not found."
					else:
						response = "530 Please log in with USER and PASS first."
					self.client.send(response)
				elif "RNFR" in command:
					if(flag == 1):
						dirc = command.strip().split('RNFR ')[1]
						if (os.path.isdir(path+"/"+dirc)):
							src = dirc
							response = "ada foldernya"
						else:
							response = "ga ada foldernya"
					else:
						response = "530 Please log in with USER and PASS first."
					self.client.send(response)
				elif "RNTO" in command:
					if(flag==1):
						if src != '':
							dst = command.strip().split('RNTO ')[1]
							os.rename(src,dst)
							response = "bisa ganti nama folder"
						else:
							response = "belum nentuin folder mana yg mau direname"
					else:
						response = "530 Please log in with USER and PASS first."	
					self.client.send(response)
			else:
				self.client.close()
				running = 0
		

if __name__ == "__main__":
	s = Server()
	s.run()