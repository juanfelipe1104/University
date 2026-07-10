#include "utils.h"
#include "FileManagerServer.h"
#include "brokermanager.h"
#include <iostream>
#include <string>
#include <thread>
#include <list>

const details serverDetails = {"127.0.0.1", 8080};

// Amazon: 98.86.76.36

void brokerRegister(details brokerDetails, details serverDetails)
{
	connection_t conn = initClient(brokerDetails.ip, brokerDetails.port);
	std::vector<unsigned char> buffer;

	pack(buffer, RegisterF);
	packString(buffer, serverDetails.ip);
	pack(buffer, (int)serverDetails.port);
	sendMSG(conn.serverId, buffer);

	buffer.clear();
}

void brokerUnregister(details brokerDetails, details serverDetails)
{
	connection_t conn = initClient(brokerDetails.ip, brokerDetails.port);
	std::vector<unsigned char> buffer;

	pack(buffer, UnregisterF);
	packString(buffer, serverDetails.ip);
	pack(buffer, (int)serverDetails.port);
	sendMSG(conn.serverId, buffer);

	buffer.clear();
}

int main(int argc, char **argv)
{
	brokerRegister(BrokerManager::brokerDetails, serverDetails);

	// init server
	int serverSocketID = initServer(serverDetails.port);
	while (1)
	{
		while (!checkClient())
			usleep(100);

		std::cout << "Cliente conectado\n";

		int clientId = getLastClientID();
		std::thread *th = new std::thread(FileManagerServer::attendClient, clientId);
	}
	brokerUnregister(BrokerManager::brokerDetails, serverDetails);
	return 0;
}
