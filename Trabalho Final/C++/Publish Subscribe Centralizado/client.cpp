#include <bits/stdc++.h>
#include <sys/types.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 
#include <netdb.h>
#include <unistd.h>
#include <pthread.h>
#define MAX_LINE 256

using namespace std;

vector<string> interests = {"Jogos", "Eleicoes", "Tempo"};

typedef struct {
	struct addrinfo *address;
	int socketID;
}connectionInformation;

connectionInformation brokerConnection(string ip, string port);

void *receiveMessage(void *sock);

void *sendMessage(void *sock);

int main(){
	srand(time(0));
	string ip, port;
	connectionInformation connection;
	pthread_t sendm, receivem;
	cout << "Digite o IP do Broker: ";
	cin >> ip;
	cout << "Digite a porta do Broker: ";
	cin >> port;
	connection = brokerConnection(ip, port);
	if(connection.socketID < 0)
		return 0;
	pthread_create(&sendm, NULL, sendMessage, (void *)(&(connection.socketID)));
	pthread_create(&receivem, NULL, receiveMessage, (void *)(&(connection.socketID)));
	pthread_join(sendm, NULL);
	pthread_join(receivem, NULL);
	return 0;
}

void *receiveMessage(void *sock){
	int socketID = *((int*)sock);
	while(1){
		char message[MAX_LINE];
		memset(message, '\0', sizeof(message));
		if(recv(socketID, message, sizeof(message), 0) < 0){
			perror("Failed to receive message");
			pthread_exit(NULL);
			return NULL;
		}
		printf("\n%s\n", message);
	}
}

void *sendMessage(void *sock){
	int socketID = *((int*)sock);
	int op;
	while(1){
		printf("1. Inscrever (Subscribe)\n2. Publicar (Publish)\n3. Auto-publicar\n4. Modo de simulacao\n5. Encerrar thread de envio\nDigite sua opcao: ");
		scanf("%d", &op);
		if(op == 1){
			char request[2] = "2", *message_c;
			string aux, message;
			printf("Lista de topicos disponiveis: \n");
			if(send(socketID, request, strlen(request), 0) < 0){
				perror("Failed to send message");
				continue;
			}	
			printf("Digite o topico a qual deseja se inscrever: ");
			cin >> aux;
			message = string("1") + string(" ") + aux;
			message_c = (char *)message.c_str();
			if(send(socketID, message_c, strlen(message_c), 0) < 0){
				perror("Failed to send message");
				continue;
			}	
		}
		else if(op == 2){
			string aux1, aux2, message;
			char *message_c;
			printf("Digite o topico em qual deseja publicar uma noticia: ");
			cin >> aux1;
			printf("Digite a noticia: ");
			cin >> aux2;
			message = string("0") + string(" ") + aux1 + " " + aux2;
			message_c = (char *)message.c_str();
			if(send(socketID, message_c, strlen(message_c), 0) < 0){
				perror("Failed to send message");
				continue;
			}	
		}
		else if(op == 3){
			string aux1, aux2;
			printf("Digite o topico em qual deseja auto-publicar noticias: ");
			cin >> aux1;
			while(1){
				char message[MAX_LINE];
				memset(message, '\0', sizeof(message));
				int num = rand()%10000;
				sprintf(message, "0 %s %cnews%d", (char *)aux1.c_str(), aux1[0], num);
				if(send(socketID, message, strlen(message), 0) < 0){
					perror("Failed to send message");
					continue;
				}	
				sleep(1);
			}
		}
		else if(op == 4){
			while(1){
				char aux1[MAX_LINE];
				memset(aux1, '\0', sizeof(aux1));
				sprintf(aux1, "%s%d", (char *)interests[rand()%interests.size()].c_str(), rand()%10);
				int op = rand()%2;
				if(op == 0){ //Publish
					char message[MAX_LINE];
					memset(message, '\0', sizeof(message));
					int num = rand()%10000;
					sprintf(message, "0 %s %cnews%d", aux1, aux1[0], num);
					if(send(socketID, message, strlen(message), 0) < 0){
						perror("Failed to send message");
						continue;
					}	
				}
				else{ //Subscribe
					char message[MAX_LINE];
					memset(message, '\0', sizeof(message));
					sprintf(message, "1 %s", aux1);
					if(send(socketID, message, strlen(message), 0) < 0){
						perror("Failed to send message");
						continue;
					}	
				}
			}
		}
		else{
			return NULL;
		}
	}
}

connectionInformation brokerConnection(string ip, string port){
	struct addrinfo hints, *brokerAddress;
	connectionInformation connection;
	int socketID;
	connection.socketID = -1;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	if(getaddrinfo(ip.c_str(), port.c_str(), &hints, &brokerAddress) != 0){
		perror("Failed to get address");
		return connection;
	}
	socketID = socket(brokerAddress->ai_family, brokerAddress->ai_socktype, brokerAddress->ai_protocol);
	if(socketID < 0){
		perror("Failed to create socket for broker connection");
		return connection;
	}
	if(connect(socketID, brokerAddress->ai_addr, brokerAddress->ai_addrlen) == -1){
		perror("Connection failed");
		return connection;
	}
	printf("Connection successful!\n");
	connection.socketID = socketID;
	connection.address = brokerAddress;
	return connection;
} 
