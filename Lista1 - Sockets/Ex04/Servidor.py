from socket import *
from decimal import *
serverPort = 12006
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
sexo, altura = message.split(' ')

altura = float(altura)
if sexo == 'masculino':
	connectionSocket.send(str(72.7*altura - 58))
else:
	connectionSocket.send(str(62.1*altura - 44.7))

connectionSocket.close()
