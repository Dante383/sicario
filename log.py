#!/usr/bin/python


# Sicario C&C Server 
# Console log module

import sicario

import datetime

def log (text):
	now = datetime.datetime.now()
	print('[{}] {}'.format(now.strftime("%Y-%m-%d %H:%M:%S"), text))