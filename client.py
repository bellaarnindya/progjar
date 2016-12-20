from socket import socket, AF_INET, SOCK_STREAM
from select import select
import sys
import threading
import os

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 21))


while True:
	reads, writes, errors = select([client_socket], [], [], 1)
	if not reads:
		break
	else:
		for read in reads:	
			msg = read.recv(1024)
			print msg,


while True:
	command = sys.stdin.readline()
	client_socket.send(command)
	if "LIST" in command:
		msg=client_socket.recv(1024)
		if msg == []:
			msgprint=msg.strip().split('\r\n')
			a=0
			b=len(msgprint)
			while a<b :
				cetak=msgprint[a].split(' ')[-1] 
				print cetak
				a+=1
		else:
			print msg
	elif "STOR" in command:
		#part = command.split()
		#fstor = ' '.join(part[1:])
		msg = client_socket.recv(1024)
		path = msg
		print path
		if(not os.path.isfile(path)):
			print "450 File not found"
			continue
		#get size
		buff = os.path.getsize(path)
		
		#buat header
		header = "file-size: "+str(buff)
		header = header+"\n"
		client_socket.send(header)

		#baca file
		baca = open(path, 'rb')
		while(buff > 0):
			box = baca.read(1024)
			client_socket.send(box)
			buff -= 1024
		baca.close()

		#get status
		status = client_socket.recv(1024)
		print status

	elif "RETR" in command:
		
		part = command.split()
		fstor = ' '.join(part[1:])
		client_socket.send(fstor)
		
		#get header
		temp_head = client_socket.recv(1024)
		#print temp_head
		
		#get size
		temp_size = temp_head.split('\n')[0]
		temp_size = temp_size.split(' ')[1]
		temp_size = int(temp_size)
		#print temp_size

		#tulis file
		# now = os.getcwd()
		#print fstor
		tulis = open("E:/SABILA/Kuliah/SEMESTER 5/PROGJAR/FINAL PROJECT/download"+"/"+fstor, 'wb')
		tanda = False
		while True:
			box = client_socket.recv(1024)
			temp_size -= 1024
			tulis.write(box)
			if(temp_size<=0):
				tanda = True
				break
		tulis.close()

		#kirim status
		if tanda == True:
			response = "226 Transfer completed"
		else:
			response = "451 Failed to transfer"
		print response
		
	elif "QUIT" in command:
		response = client_socket.recv(1024)
		print response
		client_socket.close()
		sys.exit(0)
		break
	else:	
		msg = client_socket.recv(1024)
		print msg

client_socket.close()