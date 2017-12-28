#!/usr/bin/python


# Sicario C&C Server 
# Console log module

import sicario

import datetime

now = datetime.datetime.now()

def log (text):
	print('[{}] {}'.format(now.strftime("%Y-%m-%d %H:%M:%S"), text))