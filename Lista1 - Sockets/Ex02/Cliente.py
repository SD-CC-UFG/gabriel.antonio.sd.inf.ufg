from socket import *

serverName = 'localhost'
serverPort = 12006

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

nome = raw_input('Nome: ')
sexo = raw_input('Sexo: ')
idade = raw_input('Idade: ')

message = sexo + ' ' + idade
encodedMessage = bytes(message)

clientSocket.send(encodedMessage)

resposta = clientSocket.recv(1024)
print (resposta)

clientSocket.close()
