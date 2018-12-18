from socket import *
from threading import *
import string
import random

assuntos = ['futebol','jogos','eleicao']
def aceitar_conexoes():
	while 1:
		clientSocket.listen(1000)
		client, addr = clientSocket.accept()
		Thread(target=receive, args=(client,)).start()
def receive(clientSocket):
	while 1:
		message = clientSocket.recv(1024)
		if not message:
			break
		print(message)

def send():
	
	while 1:
		print('0 - Publish\n1 - Subscribe\n2 - Request Interest List\n8 - Sair\n')
		#message = raw_input()
		#m = int(message)
		serverName, Port = address.split(' ')
		serverPort = int(Port)
		serverSocket = socket(AF_INET, SOCK_STREAM)
		serverSocket.connect((serverName,serverPort))
		m = random.randint(0,3)
		if m == 0:
			assunto = assuntos[random.randint(0,2)] + str(random.randint(0,10))
			print(assunto)
			noticia = assunto[0] + 'news' + str(random.randint(0,9999))
			print(noticia)
			tosend = str(MyPort) + ' ' +'1' + ' ' + '0' + ' ' + str(assunto) + ' ' + str(noticia)
			print(tosend)
			serverSocket.send(bytes(tosend))
			
		elif m == 1:
			assunto = str(assuntos[random.randint(0,2)])
			assunto =  assunto + str(random.randint(0,10))
			print(assunto)
			tosend = str(MyPort) + ' ' + '1' + ' ' + '1' + ' ' + str(assunto)
			print(tosend)
			serverSocket.send(bytes(tosend))
		else:
			tosend = str(MyPort) + ' ' +'1' + ' ' + '2' + '\n'
			print(tosend)
			serverSocket.send(bytes(tosend))
			serverSocket.close()
			
		
#IP e porta do servidor de nomes
serverName = 'localhost'
serverPort = 12004

#Para cliente ter uma thread esperando notificacoes
MyPort = int(raw_input('Insira a porta\n'))
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.bind(('', MyPort))
clients = {}
ends = {}
#----------------------------------

#Recebe endereco do broker
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.connect((serverName,serverPort))
serverSocket.send(bytes('c1c'))
address = serverSocket.recv(1024)
print(address)
serverSocket.close()
#--------------

th = Thread(target=aceitar_conexoes)
send_thread = Thread(target=send)
th.start()
send_thread.start()
th.join()
send_thread.join()


