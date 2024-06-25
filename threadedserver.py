# Import socket module
from socket import * 
import sys # In order to terminate the program
import threading
import time

def main():
	# Slow mode for testing
	slow = False
	if len(sys.argv) > 1:
		if '--slow' in sys.argv:
			print('Slow mode enabled')
			slow = True


	serverSocket = socket(AF_INET, SOCK_STREAM)

	# Prepare a sever socket
	serverSocket.bind(('', 56006))
	# allow up to 5 queued connections
	serverSocket.listen(5)

	try:
		while True:
			# accept connection
			connectionSocket, addr = serverSocket.accept()

			# create a new thread to handle the request
			thread = threading.Thread(target=handle, args=(connectionSocket, addr, slow))
			thread.start()
	except KeyboardInterrupt:
		# Close after keyboard interrupt
		serverSocket.close()
		sys.exit()

def handle(connectionSocket, addr, slow = False):
	try:
		message = connectionSocket.recv(1024).decode()

		# Sleep to test multiple connections
		if slow:
			time.sleep(5)

		# Ignore empty messages
		if len(message.split()) < 2:
			connectionSocket.close()
			return

		# Extract requested file path
		filename = message.split()[1]

		# redirect to default page
		if filename == '/':
			filename = '/HelloWorld.html'
		
		# Open the file
		f = open(filename[1:])
		outputdata = f.readlines()

		# send one http header line in to the socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
		connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

		# Send the content of the requested file to the connection socket
		for i in range(0, len(outputdata)):  
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send("\r\n".encode()) 
		
		connectionSocket.close()

	except IOError:
			# Send HTTP response code and message for file not found
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

			# Close the client connection socket
			connectionSocket.close()

if __name__ == '__main__':
	main()