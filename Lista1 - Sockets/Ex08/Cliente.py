from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

saldo = raw_input('Saldo Medio: ')

encodedMessage = bytes(saldo)

clientSocket.send(encodedMessage)

credito = clientSocket.recv(1024)
print ('Saldo Medio: ' + saldo)
print('Valor de credito: ' + credito)

clientSocket.close()
