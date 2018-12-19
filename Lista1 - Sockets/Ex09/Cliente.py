from socket import *

serverName = 'localhost'
serverPort = 12002

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

valorCarta = raw_input('Valor da Carta: ')
naipe = raw_input('Naipe: ')


message = valorCarta + ' ' + naipe
encodedMessage = bytes(message)

clientSocket.send(encodedMessage)

nome = clientSocket.recv(1024)
print (nome)
clientSocket.close()
