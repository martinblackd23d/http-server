# Import socket module
from socket import * 
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
serverSocket.bind(('', 56006))
serverSocket.listen(1)

while True:
	print('The server is ready to receive')

	connectionSocket, addr = serverSocket.accept()

	try:

		message = connectionSocket.recv(1024).decode()
		
		# Ignore empty messages
		if len(message.split()) < 2:
			connectionSocket.close()
			continue

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

serverSocket.close()  
sys.exit()#Terminate the program after sending the corresponding data