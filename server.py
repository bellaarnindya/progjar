import socket
import select
import sys
import threading
import os

#rani
#raras
src = ''
username = ''
#data = [{'u':'sabila', 'p': 'rani'}, {'u':'mila', 'p': 'raras'}]
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
		self.client.send('220 Welcome!\r\nSilahkan masukkan Username dan Password dahulu.\r\n')
		flag = 0
		running = 1
		base = "E:/KULIAH/SEMESTER 5/PROGJAR/progjar"
		while running:
			data = [{'u':'sabila', 'p': 'rani'}, {'u':'mila', 'p': 'raras'}]
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
						pwd = os.path.relpath(os.getcwd(), base+"/"+username)
						if pwd == '.':
							pdir = '/'
						else:
							pdir = '/'+pwd
						response = "257 \""+pdir+"\" is current directory."
						self.client.send(response)
					if "CWD" in command:
						cdir = command.strip().split('CWD ')[1]
						if (os.path.isdir(path+"/"+cdir)):
							if cdir == "..":
								cur = path.split('/')[-1]
								path = path.split("/"+cur)[0]
								if(path== base+"/"+username):
									cetak = "/"
								else:
									cetak = path.split(base+"/"+username)[1]
								os.chdir(path)
								response = "250 CWD successful. \""+cetak+"\" is current directory."
							else:
								path = path+"/"+cdir
								os.chdir(path)
								cetak = path.split(base+"/"+username)[1]
								response = "250 CWD successful. \""+cetak+"\" is current directory."
						else:
							response = "550 CWD failed. "+cdir+": directory not found."
						self.client.send(response)
					elif "QUIT" in command:
						response = "221 Goodbye."
						self.client.send(response)
						running = 0
						self.client.close()
					elif "RNFR" in command:
						dirc = command.strip().split('RNFR ')[1]
						if (os.path.isdir(path+"/"+dirc)):
							src = dirc
							response = "350 Directory exists, ready for destination name."
						else:
							response = "550 file/directory not found"				
						self.client.send(response)
					elif "RNTO" in command:
						if src:
							dst = command.strip().split('RNTO ')[1]
							os.rename(src,dst)
							response = "250 file renamed succesfully"
						else:
							response = "503 Bad sequence of commands!"
						self.client.send(response)
					elif "DELE" in command:
						dfile = command.strip().split('DELE ')[1]
						if(os.path.isfile(path+"/"+dfile)):
							os.remove(dfile)
							response = "250 File deleted successfully"
						else:
							response = "550 File not found"
						self.client.send(response)
					elif "RMD" in command:
						ddir = command.strip().split('RMD ')[1]
						if(os.path.isdir(path+"/"+ddir)):
							os.rmdir(ddir)
							response = "250 Directory deleted successfully"
						else:
							response = "550 Directory not found"
						self.client.send(response)
					elif "LIST" in command:
						cetak=''
						for file in os.listdir(path):
							cetak=cetak+"\r\n"+file
							print(file)
						self.client.send(cetak)
					elif "HELP" in command:
						self.client.send('214-The following commands are recognized:\r\nPWD\r\nCWD\r\nQUIT\r\nRETR\r\nSTOR\r\nRNTO\r\nDELE\r\nRMD\r\nMKD\r\nLIST\r\nHELP\r\n')
					elif "RETR" in command:
						# part = command.split()
						fstor = self.client.recv(1024)

						server = base+"/"+username+"/dataset/"+fstor
						# msg = self.client.recv(1024)
						# path = msg
						# print path
						if(not os.path.isfile(server)):
							print "ga ada"
							continue
						#get size
						buff = os.path.getsize(server)
						
						#buat header
						header = "file-size: "+str(buff)
						header = header+"\n"
						self.client.send(header)

						#baca file
						baca = open(server, "rb")
						while(buff > 0):
							box = baca.read(1024)
							self.client.send(box)
							buff -= 1024
						baca.close()

						#get status
						status = self.client.recv(1024)
						print status
					elif "STOR" in command:
						server = base+"/unggah/"
						part = command.split()
						fstor = ' '.join(part[1:])
						self.client.send(server+fstor)
						print server+fstor
						
						#get header
						temp_head = self.client.recv(1024)
						print temp_head
						
						#get size
						temp_size = temp_head.split('\n')[0]
						temp_size = temp_size.split(' ')[1]
						temp_size = int(temp_size)
						print temp_size

						#tulis file
						now = os.getcwd()
						tulis = open(now+"/"+fstor, 'wb')
						tanda = False
						while True:
							box = self.client.recv(1024)
							temp_size -= 1024
							tulis.write(box)
							if(temp_size<=0):
								tanda = True
								break
						tulis.close

						#kirim status
						if tanda == True:
							response = "berhasil kirim"
						else:
							response = "gagal kirim"
						self.client.send(response)


			else:
				self.client.close()
				running = 0
		

if __name__ == "__main__":
	s = Server()
	s.run()