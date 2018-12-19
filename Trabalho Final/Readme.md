
# Trabalho Final - Sistemas Distribuidos

Grupo:

André Pires Corrêa

Gabriel Antonio

Arnold Lima


Tema: Publish/Subscribe


As implementações realizadas para o trabalho consistem de duas implementações em C++ e uma em Python, referentes a um sistema Publish/Subscribe centralizado, Publish/Subscribe distribuido com algoritmo de filtragem e Publish/Subscribe distribuido com serviço de nomes, respectivamente.

Instruções de uso:

C++

Para compilar os codigos em C++, é necessario o uso do comando de compilação -lpthread.

Publish/Subscribe centralizado: Ao iniciar a execução do Broker (broker.cpp) deve ser informada a porta a ser utilizada. Para iniciar um cliente (client.cpp), deve ser informado o endereço IP e porta do Broker. Por consequencia, o Broker deve ter sido aberto antes de qualquer cliente.

Publish/Subscribe distribuido com algoritmo de filtragem: Devem ser iniciados todos os Brokers da rede de Brokers antes de conectar algum cliente, o comportamento do programa é indefinido caso contrario. Ao iniciar um Broker, você tera a opção de conecta-lo a outro Broker que já esteja executando, informando o seu IP e porta. Para o primeiro Broker a ser iniciado, deve ser escolhida a opção de não conectar a outros Brokers.


Python

Compilação em Python: python3 NomeDoPrograma.py

Publish/Subscribe distribuido com algoritmo de filtragem: O serviço de nomes, sob o nome NameServer.py, deve ser executado primeiro, em seguida, feita a inicialização dos Brokers(iniciando "n" instâncias de Broker.py) e finalmente, são instanciados os clientes, iniciando "m" instâncias de Client.py.
