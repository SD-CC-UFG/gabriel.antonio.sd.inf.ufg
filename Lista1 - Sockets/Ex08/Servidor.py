from socket import *
from decimal import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
saldo = float(message)

if saldo >= 0 and saldo <= 200:
	credito = 0
elif saldo >= 201 and saldo <= 400:
	credito = 0.2
elif saldo >= 401 and saldo <= 600:
	credito = 0.3
else:
	credito = 0.4

saldo = saldo*credito	
connectionSocket.send(str(saldo))

connectionSocket.close()
