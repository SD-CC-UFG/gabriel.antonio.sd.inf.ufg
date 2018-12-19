from socket import *

serverName = 'localhost'
serverPort = 12005

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

idade = raw_input('Idade: ')
tempo = raw_input('Tempo de servico: ')

message = idade + ' ' + tempo
encodedMessage = bytes(message)

clientSocket.send(encodedMessage)

condicao = clientSocket.recv(1024)
print ('Condicao: ' + condicao)

clientSocket.close()
