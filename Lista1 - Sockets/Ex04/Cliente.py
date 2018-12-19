from socket import *

serverName = 'localhost'
serverPort = 12006

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sexo = raw_input('Sexo: ')
altura = raw_input('Altura: ')


message = sexo + ' ' + altura
encodedMessage = bytes(message)

clientSocket.send(encodedMessage)

pesoIdeal = clientSocket.recv(1024)
print ('Peso ideal: ' + pesoIdeal)

clientSocket.close()
