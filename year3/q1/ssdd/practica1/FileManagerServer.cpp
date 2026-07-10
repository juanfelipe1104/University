#include "FileManagerServer.h"

void FileManagerServer::attendClient(int clientId)
{
	std::vector<unsigned char> buffer;
	fileFuncs option;
	do
	{
		recvMSG(clientId, buffer);
		option = unpack<fileFuncs>(buffer);

		switch (option)
		{
		case FileManagerF:
		{
			std::string dir = unpackString(buffer);

			FileManager fm(dir);
			FileManagerServer::clients[clientId] = fm;

			buffer.clear();
			pack(buffer, ackMSG);
		}
		break;

		case FileManagerDF:
		{
			FileManagerServer::clients.erase(clientId);
			buffer.clear();
			pack(buffer, ackMSG);
		}
		break;

		case listFilesF:
		{
			FileManager fm = FileManagerServer::clients[clientId];
			vector<string> files = fm.listFiles();

			buffer.clear();
			pack(buffer, ackMSG);
			pack(buffer, (int)files.size());
			for (string &file : files)
			{
				pack(buffer, (int)file.size());
				packv(buffer, (char *)file.data(), file.size());
			}
		}
		break;

		case readFileF:
		{
			FileManager fm = FileManagerServer::clients[clientId];
			std::string name = unpackString(buffer);
			std::vector<unsigned char> data;

			fm.readFile(name, data);

			buffer.clear();
			pack(buffer, ackMSG);
			pack(buffer, (int)data.size());
			packv(buffer, (unsigned char *)data.data(), (int)data.size());
		}
		break;

		case writeFileF:
		{
			FileManager fm = FileManagerServer::clients[clientId];
			std::string name = unpackString(buffer);
			vector<unsigned char> data;

			data.resize(unpack<int>(buffer));
			unpackv<unsigned char>(buffer, data.data(), data.size());
			fm.writeFile(name, data);
			buffer.clear();
			pack(buffer, ackMSG);
		}
		break;

		default:
			std::cerr << "FM: op invalida\n";
			buffer.clear();
			pack(buffer, ackMSG);
			break;
		}
		sendMSG(clientId, buffer);
	} while (option != FileManagerDF);
	closeConnection(clientId);
}