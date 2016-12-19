from socket import socket, AF_INET, SOCK_STREAM
from select import select
import sys


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
	msg = client_socket.recv(1024)
	print msg


client_socket.close()
