#!/usr/bin/python

import sicario

# Sicario C&C server
# command parser

import string

def parse (command):
	return command.split(' ') # easy

def encode (args):
	return ' '.join(str(arg) for arg in args)