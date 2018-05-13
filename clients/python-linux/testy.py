import sicario 

class Daemon: 
	def __init__ (self):
		print('chuj')

	def stop(self):
		print('fukin bicz')

sicario.Sicario(Daemon(), ['127.0.0.1', 7319, '63D185A8E7E5853D514210E0DA1D0A34', 5])