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

def main (version, args):
	log.log('Sicario C&C server {} starting...'.format(version))
	
	log.log('Starting listener at {}:{}...'.format(args.host, args.port))
	
	try:
		listener.listen(args.host, int(args.port), socket_client.Client)
	except IOError as e:
		log.log('Exception: {}'.format(e))
		log.log('Failed to start listener! Exiting..')
		sys.exit()
		
	log.log('Trying to connect to database...')
	try:
		database({'dbname':'sicario'})
	except IOError as e:
		log('Exception: {}'.format(e))
		log('Failed to connect to database! Exiting..')
		sys.exit()
	
def exit ():
	log.log('Exitting...')
	sys.exit()
	
if __name__ == '__main__':
	args = parser.parse_args()
	main(version, args)