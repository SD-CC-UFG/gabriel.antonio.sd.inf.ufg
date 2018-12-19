from socket import *

nomeCartas = [' ','as','dois','tres','quatro','cinco','seis','sete','oito','nove','dez','valete','dama','rei']
naipeCartas = [' ', 'ouros','paus','copas','espadas']

class carta:
	
	def __init__(self, valorCarta, naipe):
		self.valorCarta = valorCarta
		self.naipe = naipe
	
	def retornaNome(self):
		return nomeCartas[self.valorCarta] + ' de ' + naipeCartas[self.naipe]
	


serverPort = 12002
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('Servidor online')

connectionSocket, addr = serverSocket.accept()
message = connectionSocket.recv(1024)
valorCarta, naipe = message.split(' ')

valorCarta = int(valorCarta)
naipe = int(naipe)

cartaObj = carta(valorCarta, naipe)

message = cartaObj.retornaNome()

connectionSocket.send(message)

connectionSocket.close()
