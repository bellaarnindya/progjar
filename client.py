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
			msg = read.recv(2048)
			print msg,

commands = []
commands.append('USER progjar\r\n')
commands.append('PASS efpe\r\n')
commands.append('CWD\r\n')
commands.append('QUIT\r\n')

i = 0

while i<len(commands):
	client_socket.send(commands[i])
	msg = client_socket.recv(2048)
	print msg,
	i+=1

client_socket.close()
