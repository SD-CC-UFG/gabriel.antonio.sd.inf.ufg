from socket import *

serverName = 'localhost'
serverPort = 12005

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

idade = raw_input('Idade: ')

encodedMessage = bytes(idade)

clientSocket.send(encodedMessage)

categoria = clientSocket.recv(1024)
print ('Categoria: ' + categoria)
clientSocket.close()
