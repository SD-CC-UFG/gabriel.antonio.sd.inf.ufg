from socket import *
from decimal import *
serverPort = 12004
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
cargo, salario = message.split(' ')

salarioCorrigido = float(salario)
if cargo == 'operador':
	salarioCorrigido = salarioCorrigido + salarioCorrigido*0.20
else:
	salarioCorrigido = salarioCorrigido + salarioCorrigido*0.18

connectionSocket.send(str(salarioCorrigido))

connectionSocket.close()
