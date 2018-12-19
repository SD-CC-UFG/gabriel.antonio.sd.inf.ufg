from socket import *

serverName = 'localhost'
serverPort = 12004

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

nome = raw_input('Nome: ')
cargo = raw_input('Cargo: ')
salario = raw_input('Salario: ')

message = cargo + ' ' + salario
encodedMessage = bytes(message)

clientSocket.send(encodedMessage)

salarioCorrigido = clientSocket.recv(1024)
print ('Nome: ' + nome)
print ('Novo salario: ' + salarioCorrigido)

clientSocket.close()
