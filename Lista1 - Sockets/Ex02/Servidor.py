from socket import *

serverPort = 12006
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
sexo, idade = message.split(' ')

idade = int(idade)
if sexo == 'masculino':
	if idade >= 18:
		connectionSocket.send('Maior de idade')
	else:
		connectionSocket.send('Menor de idade')
else:
	if idade >= 21:
		connectionSocket.send('Maior de idade')
	else:
		connectionSocket.send('Menor de idade')
	
connectionSocket.close()
