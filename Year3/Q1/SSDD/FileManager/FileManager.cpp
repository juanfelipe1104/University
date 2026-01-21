#include "filemanager.h"
#include "FileManagerServer.h"
#include "utils.h"
#include "brokermanager.h"

#define SERVER_DIR "/home/juan"

details chooseServer(std::vector<details> serversList){
	details serverDetails;
	bool serverFound = false;
	int option = -1;
	while(!serverFound){
		std::cout << "Available File Manager Servers:" << std::endl;
		for(int i = 0; i < serversList.size(); i++){
			std::cout << i << ") " << serversList[i].ip << ":" << serversList[i].port << std::endl;
		}
		std::cout << "Choose a server by its number: ";
		std::cin >> option;
		std::cin.ignore();
		if(option >= 0 && option < serversList.size()){
			serverDetails = serversList[option];
			serverFound = true;
		}
		else{
			cout << "Invalid option, try again." << endl;
		}
	}
	return serverDetails;
}

details askBrokerForServer(details brokerDetails){
	connection_t conn = initClient(brokerDetails.ip, brokerDetails.port);
	std::vector<unsigned char> buffer;
	std::vector<details> serversList;
	details serverDetails;
	pack(buffer, ListServersF);
	sendMSG(conn.serverId, buffer);

	buffer.clear();
	recvMSG(conn.serverId, buffer);

	brokerFuncs ack = unpack<brokerFuncs>(buffer);
	if(ack != ackMSGF){
		cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;
	}
	else{
		int numServers = unpack<int>(buffer);
		serversList.resize(numServers);
		for(int i = 0; i < numServers; i++){
			serversList[i].ip = unpackString(buffer);
			serversList[i].port = unpack<int>(buffer);
		}
		serverDetails = chooseServer(serversList);
	}
	return serverDetails;
}

FileManager::FileManager() : FileManager(SERVER_DIR) {}

FileManager::FileManager(string path)
{
	details serverDetails = askBrokerForServer(BrokerManager::brokerDetails);
	connection_t conn = initClient(serverDetails.ip, serverDetails.port);
	vector<unsigned char> buffer;

	pack(buffer, FileManagerF);
	packString(buffer, path);
	sendMSG(conn.serverId, buffer);
	buffer.clear();
	recvMSG(conn.serverId, buffer);

	fileFuncs ack = unpack<fileFuncs>(buffer);
	if (ack != fileFuncs::ackMSG)
	{
		cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;
	}
	else
	{
		FileManagerServer::connectionIds[this] = conn;
	}
}

FileManager::~FileManager()
{
	connection_t conn = FileManagerServer::connectionIds[this];

	vector<unsigned char> buffer;
	pack(buffer, FileManagerDF);

	sendMSG(conn.serverId, buffer);
	buffer.clear();
	recvMSG(conn.serverId, buffer);

	fileFuncs ack = unpack<fileFuncs>(buffer);

	if (ack != ackMSG)
	{
		cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;
	}

	closeConnection(conn.serverId);
}

vector<string> FileManager::listFiles()
{
	std::vector<std::string> files;
	connection_t conn = FileManagerServer::connectionIds[this];

	vector<unsigned char> buffer;
	pack(buffer, listFilesF);
	sendMSG(conn.serverId, buffer);

	buffer.clear();
	recvMSG(conn.serverId, buffer);

	fileFuncs ack = unpack<fileFuncs>(buffer);
	if (ack != ackMSG)
	{
		cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;
	}
	else
	{
		int numFiles = unpack<int>(buffer);
		files.resize(numFiles);
		for (int i = 0; i < numFiles; i++)
		{
			files[i].resize(unpack<int>(buffer));
			unpackv<char>(buffer, (char *)files[i].data(), files[i].size());
		}
	}
	return files;
}

void FileManager::readFile(string fileName, vector<unsigned char> &data)
{
	connection_t conn = FileManagerServer::connectionIds[this];

	vector<unsigned char> buffer;
	pack(buffer, readFileF);
	packString(buffer, fileName);

	sendMSG(conn.serverId, buffer);

	buffer.clear();
	recvMSG(conn.serverId, buffer);

	fileFuncs ack = unpack<fileFuncs>(buffer);
	if (ack != ackMSG)
	{
		cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;
	}
	else
	{
		int numData = unpack<int>(buffer);
		data.resize(numData);
		unpackv<unsigned char>(buffer, (unsigned char *)data.data(), data.size());
	}
}

void FileManager::writeFile(string fileName, vector<unsigned char> &data)
{
	connection_t conn = FileManagerServer::connectionIds[this];
	vector<unsigned char> buffer;
	pack(buffer, writeFileF);
	packString(buffer, fileName);
	pack(buffer, (int)data.size());
	packv(buffer, (unsigned char *)data.data(), data.size());

	sendMSG(conn.serverId, buffer);

	buffer.clear();
	recvMSG(conn.serverId, buffer);

	fileFuncs ack = unpack<fileFuncs>(buffer);
	if (ack != ackMSG)
	{
		cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;
	}
}