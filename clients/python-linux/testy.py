import sicario 

class Daemon: 
	def __init__ (self):
		print('chuj')

	def stop(self):
		print('fukin bicz')

sicario.Sicario(Daemon(), ['127.0.0.1', 7319])