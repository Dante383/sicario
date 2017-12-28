#!/usr/bin/python

import sicario 
import commands
import log

# Sicario C&C server
# High level client class

import time,hashlib

class Client:
	def __init__ (self, address, socket):
		self.during_disconnect = False
		self.registered = False
		self.address = address
		self.socket = socket
	
	def on_command (self, command):
		if self.during_disconnect: return False
		
		# arguments[0] is the command name
		arguments = commands.parse(command)
		
		if self.registered == False and arguments[0] != 'register':
			self.disconnect()
			return False
		
		# is it new member? let's check if he provided his key
		if len(arguments) < 2:
			# new member
			log.log('Got new member! ({}). Generating random key..'.format(self.address))
			key = hashlib.md5(str(time.time()*100000)).hexdigest().upper()
			log.log('Key for {} generated: {}'.format(self.address, key))
			self.send_command(['set','key',key])
			
			# now, we should add this to a database
	
	def send_command (self, args):
		self.raw_send(commands.encode(args))
	
	def raw_send (self, text):
		self.socket.send(text)
		
	def disconnect (self): # why bother? he will disconnect automatically in 10 seconds
		return True