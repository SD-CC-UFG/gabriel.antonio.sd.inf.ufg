from socket import *
from decimal import *
serverPort = 12005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
idade, tempo = message.split(' ')

idade = int(idade)
tempo = float(tempo)

if idade >= 65:
	connectionSocket.send('Pode se aposentar')
elif tempo >= 30:
	connectionSocket.send('Pode se aposentar')
	
elif idade >= 60 and tempo >= 25:
	connectionSocket.send('Pode se aposentar')
else:
	connectionSocket.send('Nao pode se aposentar')

connectionSocket.close()
