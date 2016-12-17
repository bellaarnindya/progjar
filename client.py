from socket import socket, AF_INET, SOCK_STREAM
from select import select
import sys


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 21))

sys.stdout.write(client.recv(1024))
namafile = ''
i = 0

while True:
	msg = sys.stdin.readline()
	if " " in msg:
		nama_file = msg.split(' ',1)[1][:-1]
	reads, writes, errors = select([client_socket], [], [], 1)
	if not reads:
		break
	else:
		for read in reads:
			msg = read.recv(2048)
			print msg,

commands = []
commands.append('USER sabila\r\n')
commands.append('PASS rani\r\n')
#commands.append('QUIT\r\n')

i = 0

while i<len(commands):
	client_socket.send(commands[i])
	msg = client_socket.recv(1024)
	print msg,
	i+=1

client_socket.close()
