from socket import *
from decimal import *
serverPort = 12005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
idade = int(message)

if idade >= 5 and idade <= 7:
	connectionSocket.send('Infantil A')
elif idade >= 8 and idade <= 10:
	connectionSocket.send('Infantil B')
elif idade >= 11 and idade <= 13:
	connectionSocket.send('Juvenil A')
elif idade >= 14 and idade <= 17:
	connectionSocket.send('Juvenil B')
else:
	if idade >= 18:
		connectionSocket.send('Adulto')
	else:
		connectionSocket.send('Sem categoria')
		
connectionSocket.close()
