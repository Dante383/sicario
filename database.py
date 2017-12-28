#!/usr/bin/python

import sicario

# Sicario C&C server
# database controller

import sqlite3

class Database:
	def __init__ (self, config):
		try:
			self.handler = sqlite3.connect(config['dbname'])
		except:
			raise IOError('Failed to connect to {}!'.format(config['dbname']))