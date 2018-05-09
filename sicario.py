#!/usr/bin/python

import log
import listener
import socket_client
import database

version = '0.1'

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--host', dest='host',
				  help='IP address to listen at',
				  default='0.0.0.0')
parser.add_argument('--port', dest='port',
					help='Port to listen at',
					default='7319')

class Sicario:
	db_handler = False

	def __init__ (self, version, args):
		
		log.log('Sicario C&C server {} starting...'.format(version))
		
		log.log('Trying to connect to database...')
		try:
			db = database.Database({'filename':'db/sicario'})
		except IOError as e:
			log('Exception: {}'.format(e))
			log('Failed to connect to a database! Exiting..')
			sys.exit()
		log.log('Connected to database!')
		print str(db.handler)
		self.db_handler = db.handler
		
		log.log('Starting listener at {}:{}...'.format(args.host, args.port))
		
		try:
			listener.listen(args.host, int(args.port), socket_client.Client)
		except IOError as e:
			log.log('Exception: {}'.format(e))
			log.log('Failed to start listener! Exiting..')
			sys.exit()
			
		
	def get_database(self):
		print str(self.db_handler)
		return self.db_handler
		
	def exit (self):
		log.log('Exitting...')
		sys.exit()
		
if __name__ == '__main__':
	args = parser.parse_args()
	Sicario(version, args)