from socket import socket, AF_INET, SOCK_STREAM
from select import select
import sys


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 52))


while True:
	reads, writes, errors = select([client_socket], [], [], 1)
	if not reads:
		break
	else:
		for read in reads:
			if "LIST" in command:
				msg=read.recv(1024)
				msgprint=msg.strip.split('\r\n')
				a=0
				b=len(msgprint)
				while a<b :
					cetak=msgprint[a].split(' ')[-1] 
					print cetak
					a+=1
			elif "221" in command:
				client_socket.close()
				sys.exit(0)
				break	
			msg = read.recv(1024)
			print msg,


while True:
	command = sys.stdin.readline()
	client_socket.send(command)
	msg = client_socket.recv(1024)
	print msg


client_socket.close()