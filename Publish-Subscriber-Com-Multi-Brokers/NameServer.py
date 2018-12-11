#c1c cliente
#c2c broker
from socket import *
from threading import *
import random
import string

def aceitar_conexoes():
	while 1:
		client, addr = serverSocket.accept()
		print(str(addr) + ' conectado')
		message = client.recv(2048).decode()
		arguments = message.split(' ')
		if arguments[0] == 'c1c':
			Thread(target=cliente, args=(client,)).start()
		else:
			Thread(target=broker, args=(client,str(arguments[1]), str(arguments[2]))).start()
		
def cliente(client):
	
	key, value = random.choice(list(brokers_list.items()))
	client.send(value.encode())
	client.close()
	
def broker(client,name, port):
	addr = str(client.getpeername()[0]) + ' ' + port
	print(addr)
	print(name)
	brokers_list[name] = addr
	
	if len(brokers_list) > 0:
		for k,v in brokers_list.items():
			if k != name:
				client.send(v.encode())
		
	client.close()
	print(brokers_list)
	
			
			
serverPort = 12004
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
brokers_list = {}


if __name__ == "__main__":
	serverSocket.listen(1000)
	print ('Servidor online')
	th = Thread(target=aceitar_conexoes)
	th.start()
	th.join()
	serverSocket.close()



