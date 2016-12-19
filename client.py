import socket
import sys


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 22))

sys.stdout.write(client.recv(1024))
sys.stdout.write('>>')

data_port = 0
nama_file = ''
i = 0

try:
#	while True:
#		reads, writes, errors = select([client_socket], [], [], 1)
#		if not reads:
#			break
#		else:
#			for read in reads:
#				msg = read.recv(1024)
#				print msg,
	while True:
		command = sys.stdin.readline()
		if " " in command:
			nama_file = command.split(' ',1)[1][:-1]
		if i==0:
			if "USER" not in command:
				client.send("USER anonymous")
				pesan = client.recv(1024)
				sys.stdout.write(pesan)
				if "331" in pesan:
					client.send("PASS ****")
					pesan = client.recv(1024)
					sys.stdout.write(pesan)
					print "Could't to connect server"
			else:
				client.send(command)
				pesan = client.recv(1024)
				sys.stdout.write(pesan)
		else:
			client.send(command)
			pesan = client.recv(1024)
			sys.stdout.write(pesan)
		if "221" in pesan:
			client.close()
			sys.exit(0)
			break
		if "530" in pesan:
			client.close()
			sys.exit(0)
		sys.stdout.write('>>')
		i+=1
#		client_socket.send(command)
#		msg = client_socket.recv(1024)
#		print msg

#client_socket.close()

except KeyboardInterrupt:
	client.close()

	sys.exit(0)
