#!/usr/bin/python

import sicario
import socket_client

# Sicario C&C server
# telnet listener

import socket
import threading
import sys

sema = threading.Lock()
threads = []

def listen (host, port, module_manager):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	s.bind((host, port))
	try:
		while True:
			s.listen(4)
			(client, address) = s.accept()
			new_thread = socket_client.Client(client, sema, module_manager)
			new_thread.start()
			threads.append(new_thread)
	except KeyboardInterrupt:
		for t in threads:
			t.stop()
		sys.exit()
	
	for t in threads:
		t.join()