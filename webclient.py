from socket import *
import sys

def main():
	if len(sys.argv) < 3:
		print('Usage: python3 webclient.py <server_host> <server_port> <filename>')
		sys.exit(1)

	# Get arguments
	server_host = sys.argv[1]
	server_port = int(sys.argv[2])
	if server_port < 1 or server_port > 65535:
		print('Invalid port')
		sys.exit(1)
	filename = sys.argv[3]
	if filename == '/':
		filename = ''

	# Create a client socket
	client_socket = socket(AF_INET, SOCK_STREAM)
	try:
		client_socket.connect((server_host, server_port))
	except ConnectionRefusedError:
		print('Connection refused')
		sys.exit(1)
	except gaierror:
		print('invalid host')
		sys.exit(1)
	
	# Send request
	client_socket.send(f'GET /{filename} HTTP/1.1\r\n'.encode())

	# Receive response
	message = ''
	while True:
		response = client_socket.recv(1024).decode()
		message += response
		if not response:
			break
	client_socket.close()
	
	# Parse response
	message = message.split('\r\n\r\n')
	headers = message[0].split('\r\n')
	status = headers[0]
	status_code = status.split()[1]
	headers = headers[1:]
	body = message[1]

	# Print response
	if status_code == '200':
		print('200 OK\n')
		print(body)
	elif status_code == '404':
		print('404 Not Found\n')
		print(body)
	else:
		print('Invalid response')

if __name__ == '__main__':
	main()