from socket import *
from decimal import *
serverPort = 12005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
nivel, salario, dependentes = message.split(' ')

salarioLiquido = float(salario)
if nivel == 'A':
	if dependentes == 0:
		salarioLiquido = salarioLiquido - salarioLiquido*0.03
	else:
		salarioLiquido = salarioLiquido - salarioLiquido*0.08
elif nivel == 'B':
	if dependentes == 0:
		salarioLiquido = salarioLiquido - salarioLiquido*0.05
	else:
		salarioLiquido = salarioLiquido - salarioLiquido*0.1
elif nivel == 'C':
	if dependentes == 0:
		salarioLiquido = salarioLiquido - salarioLiquido*0.08
	else:
		salarioLiquido = salarioLiquido - salarioLiquido*0.15
else:
	if dependentes == 0:
		salarioLiquido = salarioLiquido - salarioLiquido*0.10
	else:
		salarioLiquido = salarioLiquido - salarioLiquido*0.17
	
connectionSocket.send(str(salarioLiquido))

connectionSocket.close()
