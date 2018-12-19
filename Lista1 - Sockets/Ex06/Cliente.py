from socket import *

serverName = 'localhost'
serverPort = 12005

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

nome = raw_input('Nome: ')
nivel = raw_input('Nivel: ')
salario = raw_input('Salario bruto: ')
dependentes = raw_input('Dependentes: ')

message = nivel + ' ' + salario + ' ' + dependentes
encodedMessage = bytes(message)

clientSocket.send(encodedMessage)

salarioLiquido = clientSocket.recv(1024)
print ('Nome: ' + nome)
print('Nivel: ' + nivel)
print ('Salario liquido: ' + salarioLiquido)

clientSocket.close()
