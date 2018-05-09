#!/usr/bin/python

import sicario

# Sicario C&C server
# telnet listener

import socket
import threading
import sys

sema = threading.Lock()
threads = []

def listen (host, port, socketClient):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	s.bind((host, port))
	try:
		while True:
			s.listen(4)
			(client, address) = s.accept()
			new_thread = socketClient(client, sema)
			new_thread.start()
			threads.append(new_thread)
	except KeyboardInterrupt:
		for t in threads:
			t.stop()
		sys.exit()
	
	for t in threads:
		t.join()