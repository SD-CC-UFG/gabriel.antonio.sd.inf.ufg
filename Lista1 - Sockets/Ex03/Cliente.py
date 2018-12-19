from socket import *

serverName = 'localhost'
serverPort = 12005

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

N1 = raw_input('N1: ')
N2 = raw_input('N2: ')
N3 = raw_input('N3: ')

message = N1 + ' ' + N2 + ' ' + N3
encodedMessage = bytes(message)

clientSocket.send(encodedMessage)
resposta = clientSocket.recv(1024)
print ('Condicao: ' + resposta)

clientSocket.close()
