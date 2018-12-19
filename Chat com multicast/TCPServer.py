from socket import *
from threading import *

def aceitar_conexoes():
	while 1:
		client, addr = serverSocket.accept()
		print(str(addr) + ' conectado')
		client.send(bytes('Ola! Digite o seu nome: '))
		ends[client] = addr
		Thread(target=cliente, args=(client,)).start()
		
def cliente(client):
	
	nome = client.recv(1024)
	clients[client] = nome
	sendall('%s se juntou ao chat' % nome, client)
	flag = True
	while flag:
		message = client.recv(1024)
		if message == '{q}':
			client.send(bytes('{q}'))
			client.close()
			del clients[client]
			sendall('%s saiu' % nome, client)
			break
		else:
			sendall(str(clients[client]) + ': ' + message, client)
			
			
def sendall(message, client):
	for cl in clients:
		if cl != client:
			cl.send(bytes(message))
			
serverPort = 12004
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
clients = {}
ends = {}


if __name__ == "__main__":
	serverSocket.listen(2)
	print ('Servidor online')
	th = Thread(target=aceitar_conexoes)
	th.start()
	th.join()
	serverSocket.close()



