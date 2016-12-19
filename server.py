import socket
import select
import sys
import threading
import os

#rani
#raras
data = [{'u':'sabila', 'p': 'rani'}, {'u':'mila', 'p': 'raras'}]
src = ''
username = ''
class Server:
	def __init__(self):
		self.host = 'localhost'
		self.port = 52
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
		flag = 0
		running = 1
		base = "E:/KULIAH/SEMESTER 5/PROGJAR/progjar"
		while running:
			command = self.client.recv(self.size)
			print 'recv: ', self.address, command
			if command:
				print flag
				if(flag==0):
					if "USER" in command:
						username = command.strip().split(' ')[1]
						#print username
						response = "331 Password required for "+username
					elif "PASS" in command:
						password = command.strip().split(' ')[1]
						#print password
						i=0
						while i<len(data):
							if (data[i]['u'] == username and data[i]['p']==password):
								response = "230 Logged on\r\n"
								os.chdir(base+"/"+username)
								path = base+"/"+username
								flag = 1
								break
							elif (i+1 == len(data)):
								response = "530 Login or password incorrect!"
								username = ''
							i+=1
					else:
						response = "530 Please log in with USER and PASS first."
					self.client.send(response)
				elif(flag==1):
					if "PWD" in command:
						response = "257 \""+pdir+"\" is current directory."
						self.client.send(response)
					elif "CWD" in command:
						print path
						last = os.getcwd()
						cdir = command.strip().split('CWD ')[1]
						if (os.path.isdir(path+"/"+cdir)):
							if cdir == "..":
								path = last.split('')[-1]
								print path
								print last
								cwd = last.split(path)[0]
								print cwd
								response = "250 CWD successful. \"/"+cwd+" is current directory."
							else:
								os.chdir(path+"/"+cdir)
								path = path+"/"+cdir
								response = "250 CWD successful. "+cdir+" is current directory."
						else:
							response = "550 CWD failed. "+cdir+": directory not found."
						self.client.send(response)
					elif "RNFR" in command:
						dirc = command.strip().split('RNFR ')[1]
						if (os.path.isdir(path+"/"+dirc)):
							src = dirc
							response = "ada foldernya"
						else:
							response = "ga ada foldernya"				
						self.client.send(response)
					elif "RNTO" in command:
						if src != '':
							dst = command.strip().split('RNTO ')[1]
							os.rename(src,dst)
							response = "bisa ganti nama folder"
						else:
							response = "belum nentuin folder mana yg mau direname"
						self.client.send(response)
					elif "DELE" in command:
						dfile = command.strip().split('DELE ')[1]
						if(os.path.isfile(path+"/"+dfile)):
							os.remove(dfile)
							response = "udah keapus"
						else:
							response = "ga ada filenya"
						self.client.send(response)
					elif "RMD" in command:
						ddir = command.strip().split('RMD ')[1]
						if(os.path.isdir(path+"/"+ddir)):
							os.rmdir(ddir)
							response = "direktori terhapus"
						else:
							response = "Tidak ada direktori"
						self.client.send(response)
					elif "MKD" in command:
						ddir = command.strip().split('MKD ')[1]
						newpath=path+"/"+ddir
						if not os.path.exists(newpath):
							os.mkdir(newpath)
							response = "direktori terbuat"
						else:
							response = "Direktori sudah ada"
						self.client.send(response)
					elif "LIST" in command:
						cetak=''
						for file in os.listdir(path):
							cetak=cetak+"\r\n"+file
							print(file)
						self.client.send(cetak)
			else:
				self.client.close()
				running = 0
		

if __name__ == "__main__":
	s = Server()
	s.run()
