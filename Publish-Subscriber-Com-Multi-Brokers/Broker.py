from socket import *
from threading import *
import string
import sys
#arguments: porta;0-broker/1-cliente;0-pub/1-sub/2-req;assunto(menos para o tipo 2);noticia apenas tipo 0 necessita.

def envia_nome(name, port):
	NameServer = 'localhost'
	NameServerPort = 12004
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((NameServer,NameServerPort))
	msg = 'c2c ' + name + ' ' + str(port)
	clientSocket.send(msg.encode())
	while 1:
		neighbours_message = clientSocket.recv(2048).decode()
		if not neighbours_message:
			break
		else:
			neighbours.append(neighbours_message) 
	clientSocket.close()
	
	for x in neighbours:
		ip, portdest = x.split(' ')
		int_port = int(portdest)
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((ip,int_port))
		msg = str(clientSocket.getsockname()[0]) + " " + str(port) + ' c3c'
		clientSocket.send(msg.encode())
		clientSocket.close()
	
def aceitar_conexoes():
	while 1:
		client, addr = serverSocket.accept()
		
		print(str(addr) + ' conectado')
		message = client.recv(2048).decode()
		arguments = message.split(' ')
		print(arguments)
		address = str(client.getsockname()[0]) + ' ' + arguments[0]
		if arguments[2] == 'c3c':
			neighbours.append(arguments[0] + " " + arguments[1])
			print("Novos vizinhos sao: ", neighbours)
		elif arguments[2] == '0': 
			Thread(target=publish, args=(arguments[3], arguments[4],address,int(arguments[1]),client)).start()
		elif arguments[2] == '1':
			Thread(target=subscribe, args=(arguments[3],address,int(arguments[1]),client)).start()
		elif arguments[2] == '2':
			Thread(target=request_insterest, args=(address,client)).start()
		#client.close() Tirei
def publish(e1,e2,x,Type,clientSocket):
	if e1 in subscriptions.keys():
		matchlist = match(e1, subscriptions)
		notify(e1,e2, matchlist)
	elif e1 not in routing.keys():
		send = []
		send.append(x)
		msg = 'Inscreva-se em ' + e1 + ' antes de publicar.\n'
		notify(e1,msg,send)		
	elif e1 in routing.keys():
		fwdlist = match(e1,routing)
		if fwdlist==[]: return
		print(fwdlist)
		print(routing)
		for p in fwdlist:
			if len(p)==1: p=fwdlist
			if p == x: continue			
			ip, port = p.split(' ')
			int_port = int(port)
			clientSocket = socket(AF_INET, SOCK_STREAM)
			clientSocket.connect((ip,int_port))
			msg = str(port) + ' 0' +' 0 ' + e1 + ' ' + e2
			clientSocket.send(msg.encode())
			clientSocket.close()
	
def subscribe(s,x,Type,clientSocket):
	if s not in routing.keys() and Type==1:
		print("1///////////////////////")
		if s not in subscriptions.keys():
			subscriptions[s]=[]
		if x not in subscriptions[s]:
			subscriptions[s].append(x)
		for p in neighbours:
			if p == x: continue
			ip, port = p.split(' ')
			int_port = int(port)
			clientSocket = socket(AF_INET, SOCK_STREAM)
			clientSocket.connect((ip,int_port))
			msg = str(MyPort) + ' 0' +' 1 ' + s
			clientSocket.send(msg.encode())
			clientSocket.close()
			
	elif s not in routing.keys() and s not in subscriptions.keys() and Type==0:
	#elif s not in routing.keys() and Type==0:
		print("2///////////////////////")
		routing[s]=x
		for p in neighbours:
			if p == x: continue
			ip, port = p.split(' ')
			int_port = int(port)
			clientSocket = socket(AF_INET, SOCK_STREAM)
			clientSocket.connect((ip,int_port))
			msg = str(MyPort) + ' 0' +' 1 ' + s
			clientSocket.send(msg.encode())
			clientSocket.close()
			
	elif s not in routing.keys() and s in subscriptions.keys() and Type==0:
	#elif s not in routing.keys() and Type==0:
		print("2333///////////////////////")
		if s not in subscriptions.keys():
			subscriptions[s]=[]
		if x not in subscriptions[s]:
			subscriptions[s].append(x)
		for p in neighbours:
			if p == x: continue
			ip, port = p.split(' ')
			int_port = int(port)
			clientSocket = socket(AF_INET, SOCK_STREAM)
			clientSocket.connect((ip,int_port))
			msg = str(MyPort) + ' 0' +' 1 ' + s
			clientSocket.send(msg.encode())
			clientSocket.close()
	
	elif s in routing.keys() and Type==1:
		print("3///////////////////////")
		p = routing[s]
		print("P é: ", p)
		portaCliente = str(clientSocket.getsockname()[1])
		portaCliente2 = str(clientSocket.getpeername()[1])
		print(portaCliente, portaCliente2, s, x)
		ip, port = p.split(' ')
		int_port = int(port)
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((ip,int_port))
		msg = (x.split(' '))[1] + ' 0' +' 1 ' + s
		clientSocket.send(msg.encode())
		clientSocket.close()
		return
		
	elif s not in routing.keys() and Type==1:
		print("4///////////////////////")
		if s not in subscriptions.keys():
			subscriptions[s]=[]
		if x not in subscriptions[s]:
			subscriptions[s].append(x)
		for p in neighbours:
			if p == x: continue
			ip, port = p.split(' ')
			int_port = int(port)
			clientSocket = socket(AF_INET, SOCK_STREAM)
			clientSocket.connect((ip,int_port))
			msg = str(MyPort) + ' 0' +' 1 ' + s
			clientSocket.send(msg.encode())
			clientSocket.close()
			
		
	elif s in routing.keys() and Type==0:
		print("5///////////////////////")
		return
	print("Lista de Roteamento")	
	print(routing)
	print("Lista de Inscrições")
	print(subscriptions)
	

def request_insterest(addr,client):
	interest_list = []
	for key,value in subscriptions.items():
		if addr in value:
			interest_list.append(key)
	
	message = ' '.join(interest_list)
	ip, port = addr.split(' ')
	int_port = int(port)
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((ip,int_port))
	clientSocket.send(message.encode())
	clientSocket.close()
	
def notify(e1,e2,matchlist):
	message = 'Assunto: ' + e1 + ' Noticia: ' + e2
	for p in matchlist:
		ip, port = p.split(' ')
		int_port = int(port)
		print("Noticação em: " + ip +'/'+ str(int_port))
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((ip,int_port))
		clientSocket.send(message.encode())
		clientSocket.close()
	
def match(e,lst):
	return lst[e]
	

routing = {}
subscriptions = {}
neighbours = []

if __name__ == "__main__":
	
	name = input('Insira o nome do broker\n')
	global MyPort
	MyPort = int(input('Insira a porta do broker\n'))
	envia_nome(name, MyPort)
	
	
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', MyPort))
	serverSocket.listen(1000)
	print ('Broker Online')
	th = Thread(target=aceitar_conexoes)
	th.start()
	th.join()
	serverSocket.close()



