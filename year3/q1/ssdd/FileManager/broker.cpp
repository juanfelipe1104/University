#include "brokermanager.h"

static void attend(int clientId)
{
	std::vector<unsigned char> buffer;
	recvMSG(clientId, buffer);
	brokerFuncs option = unpack<brokerFuncs>(buffer);

	switch (option)
	{
	case RegisterF:
	{
		std::string ip = unpackString(buffer);
		int port = unpack<int>(buffer);
		BrokerManager::registerServer(ip, port);
		buffer.clear();
		pack(buffer, ackMSGF);
	}
	break;

	case UnregisterF:
	{
		std::string ip = unpackString(buffer);
		int port = unpack<int>(buffer);
		BrokerManager::unregisterServer(ip, port);
		buffer.clear();
		pack(buffer, ackMSGF);
	}
	break;

	case ListServersF:
	{
		std::vector<details> serversList = BrokerManager::listServers();
		buffer.clear();
		pack(buffer, ackMSGF);
		pack(buffer, (int)serversList.size());
		for(details &serverDetails : serversList){
			packString(buffer, serverDetails.ip);
			pack(buffer, serverDetails.port);
		}
	}
	break;
	case GetServerF:
	{
		details serverDetails = BrokerManager::getServerDetails();
		buffer.clear();
		pack(buffer, ackMSGF);
		packString(buffer, serverDetails.ip);
		pack(buffer, serverDetails.port);
	}
	break;
	}
	sendMSG(clientId, buffer);
	closeConnection(clientId);
}

int main(int argc, char **argv)
{
	// init server
	int brokerSocketID = initServer(BrokerManager::brokerDetails.port);
	while (1)
	{
		while (!checkClient())
			usleep(100);

		std::cout << "Cliente conectado\n";

		int clientId = getLastClientID();
		std::thread *th = new std::thread(attend, clientId);
	}
	return 0;
}
