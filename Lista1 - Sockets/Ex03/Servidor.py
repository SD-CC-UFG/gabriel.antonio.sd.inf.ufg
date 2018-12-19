from socket import *

serverPort = 12005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
N1, N2, N3 = message.split(' ')
N1 = float(N1)
N2 = float(N2)
N3 = float(N3)
M = (N1 + N2)/2
if M >= 7.0:
	connectionSocket.send('Aprovado')
elif M > 3.0 and M < 7.0:
	if (M + N3)/2 >= 5.0:
		connectionSocket.send('Aprovado')
	else:
		connectionSocket.send('Reprovado')
else:
	connectionSocket.send('Reprovado')

connectionSocket.close()
