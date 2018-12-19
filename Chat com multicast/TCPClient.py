from socket import *
from threading import *

def receive():
	
	while 1:
		message = clientSocket.recv(1024)
		if message == '{q}':
			clientSocket.close()
			break
		print(message)	

def send():
	
	while 1:
		message = raw_input()
		encodedMessage = bytes(message)
		clientSocket.send(encodedMessage)
		if message == '{q}':
				break
		
		
serverName = 'localhost'
serverPort = 12004

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()


