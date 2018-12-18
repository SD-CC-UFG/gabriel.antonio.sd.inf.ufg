#include <bits/stdc++.h>
#include <sys/types.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 
#include <netdb.h>
#include <unistd.h>
#include <pthread.h>
#define MAX_PENDING 20
#define MAX_LINE 256
#define MAX_NEWS 10

typedef struct {
	struct addrinfo *address;
	int socketID;
}connectionInformation;

using namespace std;

vector<connectionInformation> connections;

vector<int> sockets;
set<int> neighborBrokers;

pthread_mutex_t pubMutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t subMutex = PTHREAD_MUTEX_INITIALIZER;
pthread_rwlock_t nbRwLock = PTHREAD_RWLOCK_INITIALIZER;//READ WRITE LOCK FOR neighborBrokers
pthread_rwlock_t fwdRwLock = PTHREAD_RWLOCK_INITIALIZER; //READ WRITE LOCK FOR forwardingTable

//------------------------------
map<string, deque<string> > newsTable;
map<string, vector<int> > interestTable;
map<string, set<int> > forwardingTable;
int operationCounter;
//------------------------------

void acceptNewConnections(int port);

void *connectionHandler(void *sock);

void publish(void *input);

bool subscribe(int socketID, char* subject_c);

void notify(string subject, string newsContent, int socketID);

void sendInterestList(int socketID);

void *statistics(void *nothing);

void connectToBrokers();

int main(){
	operationCounter = 0;
	int port;
	printf("Digite o numero da porta a ser utilizada: ");
	scanf("%d", &port);
	connectToBrokers();
	pthread_t statisticsThread;
	pthread_create(&statisticsThread, NULL, statistics, NULL);
	acceptNewConnections(port);
	return 0;
}

void notify(string subject, string newsContent, int socketID){
	vector<int> clientsToNotify = interestTable[subject];
	string message = "Assunto: " + subject + ", Noticia: " + newsContent;
	char *message_c = (char *)message.c_str();
	if(socketID == -1){
		for(uint cont = 0 ; cont < clientsToNotify.size() ; cont++){
			if(clientsToNotify[cont] != -1 && send(clientsToNotify[cont], message_c, strlen(message_c), 0) < 0){
				perror("Failed to send message, removing client from list");
				pthread_mutex_lock(&subMutex);
				close(interestTable[subject][cont]);
				interestTable[subject][cont] = -1;
				pthread_mutex_unlock(&subMutex);
			}
		}	
	}
	else{
		if(send(socketID, message_c, strlen(message_c), 0) < 0){
			perror("Failed to send message");
		}
	}
}

void notifyBrokers(int socketID, string subject, string newsContent){
	//ACQUIRING READ LOCK
	pthread_rwlock_rdlock(&fwdRwLock);
	vector<int> deadBrokers;
	set<int>::iterator it;
	string message = string("0") + string(" ") + subject + " " + newsContent;
	for(it = forwardingTable[subject].begin() ; it != forwardingTable[subject].end() ; ++it){
		int brokerSocketID = *it;
		if(brokerSocketID == socketID)
			continue;
		if(send(brokerSocketID, message.c_str(), strlen(message.c_str()), 0) < 0){
			perror("Failed to send message");
			close(brokerSocketID);
			deadBrokers.push_back(brokerSocketID);
		}
	}
	
	pthread_rwlock_unlock(&fwdRwLock);
	//UNLOCKING READ LOCK
	if(deadBrokers.size() > 0){
		//ACQUIRING WRITE LOCK
		pthread_rwlock_wrlock(&fwdRwLock);
		for(uint cont = 0 ; cont < deadBrokers.size() ; cont++){
			forwardingTable[subject].erase(deadBrokers[cont]);
		}
		pthread_rwlock_unlock(&fwdRwLock);
		//UNLOCKING WRITE LOCK
	}
}


void publish(int socketID, void *input){
	char *subject_c, *newsContent_c;
	string subject, newsContent;
	int inputLength = strlen((char *)input);
	subject_c = (char *)malloc(inputLength * sizeof(char));
	newsContent_c = (char *)malloc(inputLength * sizeof(char));
	sscanf((char *)input, "%s %s", subject_c, newsContent_c);
	subject = string(subject_c);
	newsContent = string(newsContent_c);
	free(subject_c);
	free(newsContent_c);
	
	//MUTEX LOCKED
	pthread_mutex_lock(&pubMutex);
	//newsTable[subject] = newsContent;
	if(newsTable[subject].size() < MAX_NEWS){
		newsTable[subject].push_back(newsContent);
	}
	else{
		newsTable[subject].pop_front();
		newsTable[subject].push_back(newsContent);
	}
	pthread_mutex_unlock(&pubMutex);
	//MUTEX UNLOCKED
	
	notify(subject, newsContent, -1);
	notifyBrokers(socketID, subject, newsContent);
}

void sendInterestList(int socketID){
	char message[MAX_LINE];
	memset(message, '\0', sizeof(message));
	map<string, vector<int> >::iterator it;
	
	pthread_mutex_lock(&subMutex);
	for(it = interestTable.begin() ; it != interestTable.end(); it++){
		char *value = (char *)(it->first).c_str();
		if(strlen(value) + strlen(message) + 2 < MAX_LINE){
			sprintf(message, "%s\n", value);
		}
		else
			break;
	}
	pthread_mutex_unlock(&subMutex);
	
	if(send(socketID, message, strlen(message), 0) < 0){
		perror("Failed to send message");
	}
}

bool subscribe(int socketID, char* subject_c){
	bool aux = false;
	string subject = string(subject_c);
	pthread_mutex_lock(&subMutex);
	vector<int>::iterator it = find(interestTable[subject].begin(), interestTable[subject].end(), socketID);
	if(it == interestTable[subject].end()){
		interestTable[subject].push_back(socketID);
		aux = true;
	}
	pthread_mutex_unlock(&subMutex);
	if(aux){
		for(uint cont = 0 ; cont < newsTable[subject].size() ; cont++){
			notify(subject, newsTable[subject][cont], socketID);
		}
	}
	return aux;
}

void sendSubToNeighbors(int socketID, char *sub){
	set<int>::iterator it;
	string message = string("3") + string(" ") + sub;
	vector<int> deadBrokers;
	//ACQUIRING READ LOCK
	pthread_rwlock_rdlock(&nbRwLock);
	for(it = neighborBrokers.begin() ; it != neighborBrokers.end() ; ++it){
		int brokerSocketID = *it;
		if(brokerSocketID == socketID)
			continue;
		if(send(brokerSocketID, message.c_str(), strlen(message.c_str()), 0) < 0){
			perror("Failed to send message");
			close(brokerSocketID);
			deadBrokers.push_back(brokerSocketID);
		}
	}
	pthread_rwlock_unlock(&nbRwLock);
	//UNLOCKING READ LOCK
	if(deadBrokers.size() > 0){
		//ACQUIRING WRITE LOCK
		pthread_rwlock_wrlock(&nbRwLock);
		for(uint cont = 0 ; cont < deadBrokers.size() ; cont++){
			neighborBrokers.erase(deadBrokers[cont]);
		}
		pthread_rwlock_unlock(&nbRwLock);
		//UNLOCKING WRITE LOCK
	}
}

bool addSubToForwardingTable(int socketID, char *sub){
	string topic = sub;
	//ACQUIRING WRITE LOCK
	pthread_rwlock_wrlock(&fwdRwLock);
	bool retval = (forwardingTable[topic].insert(socketID)).second;
	pthread_rwlock_unlock(&fwdRwLock);
	//UNLOCKING WRITE LOCK
	return retval;
}

void *connectionHandler(void *sock){
	string lastRequest, aux;
	int repeatedRequests = 0;
	int socketID = *((int*)sock);
	char input[MAX_LINE]; 
	while(1){
		if(repeatedRequests > 1000){
			perror("Something bad happened");
			close(socketID);
			pthread_exit(NULL);
			break;
		}
		memset(input, '\0', sizeof(input));
		int callType;
		if(recv(socketID, input, sizeof(input), 0) < 0){
			perror("Failed to receive message");
			close(socketID);
			pthread_exit(NULL);
			break;
		}
		aux = string(input);
		if(lastRequest != aux){
			lastRequest = aux;
			repeatedRequests = 0;
		}
		else{
			repeatedRequests++;
		}
		sscanf(input, "%d", &callType);
		if(callType == 0){ //Publish
			operationCounter++;
			publish(socketID, (void *)(input+2));
		}
		else if(callType == 1){ //Subscribe
			operationCounter++;
			if(subscribe(socketID, (input+2))) 
				sendSubToNeighbors(socketID, (input+2));
		}
		else if(callType == 2){ //Request Interest List
			operationCounter++;
			sendInterestList(socketID);
		}
		else if(callType == 3){ //Received Subscription from another Broker
			operationCounter++;
			if(addSubToForwardingTable(socketID, (input+2)))
				sendSubToNeighbors(socketID, (input+2));
		}
	}
	return NULL;
}

void acceptNewConnections(int port){
	struct sockaddr_in myAddress, clientAddress;
	int socketID, newSocketID;
	socklen_t clientAddressLength = sizeof(clientAddress);
	bzero((char *)&myAddress, sizeof(myAddress)); 
	myAddress.sin_family = AF_INET;
	myAddress.sin_addr.s_addr = INADDR_ANY;
	myAddress.sin_port = htons(port);
	socketID = socket(AF_INET, SOCK_STREAM, 0);
	if(socketID < 0){
		perror("Failed to create a socket");
		return;
	}
	if(bind(socketID, (struct sockaddr *)&myAddress, sizeof(myAddress)) < 0){
		perror("Failed to bind socket");
		return;
	}
	listen(socketID, MAX_PENDING);
	while(1){
		newSocketID = accept(socketID, (struct sockaddr *)&clientAddress, &clientAddressLength);
		if(newSocketID < 0){
			perror("Failed to create socket for incoming client");
			continue;
			//return;
		}
		printf("Connection successful!\n");
		
		
		//The purpose of this section is to identify if the incoming connection is another Broker or a Client.
		char input[MAX_LINE]; 
		memset(input, '\0', sizeof(input));
		int connectionType;
		if(recv(newSocketID, input, sizeof(input), 0) < 0){
			perror("Failed to receive message");
			close(newSocketID);
			continue;
			//break;
		}
		sscanf(input, "%d", &connectionType);
		if(connectionType == 1){ //if connection is another broker
			neighborBrokers.insert(newSocketID);
		}
		//
		
		sockets.push_back(newSocketID);
		pthread_t newThread;
		pthread_create(&newThread, NULL, connectionHandler, (void *)&newSocketID);
	}
}

void *statistics(void *nothing){
	while(1){
		sleep(1);
		printf("Number of procedures called in the last second: %d\n", operationCounter);
		operationCounter = 0;
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
	
	//Sending connection type information to broker
	char message[] = "1";
	if(send(socketID, message, strlen(message), 0) < 0){
		perror("Failed to send message");
		//continue;
	}	
	//
	
	return connection;
} 

void connectToBrokers(){
	string ip, port;
	connectionInformation connection;
	int op;
	printf("Estabelecer conexao com outros Brokers?\n1. Sim\n2. Nao\nOpcao: ");
	scanf("%d", &op);
	if(op != 1){
		return;
	}
	while(1){
		cout << "Digite o IP do Broker: ";
		cin >> ip;
		cout << "Digite a porta do Broker: ";
		cin >> port;
		connection = brokerConnection(ip, port);
		//neighborBrokers.push_back(connection);
		connections.push_back(connection);
		cout << "Conectar a mais algum Broker?\n1. Sim\n2. Nao\nOpcao: ";
		cin >> op;
		if(op != 1) break;
	}
	for(uint cont = 0 ; cont < connections.size() ; cont++){
		pthread_t newThread;
		neighborBrokers.insert(connections[cont].socketID);
		pthread_create(&newThread, NULL, connectionHandler, (void *)&(connections[cont].socketID));
	}
}

