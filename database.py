#!/usr/bin/python

import sicario

# Sicario C&C server
# database controller

import sqlite3

class Database:
	handler = False
	cursor = False
	
	def __init__ (self, config):
		try:
			self.handler = sqlite3.connect(config['filename'])
		except:
			self.handler = False
			raise IOError('Failed to connect to {}!'.format(config['filename']))
		self.cursor = self.handler.cursor()

	def getHandler (self):
		return self.handler