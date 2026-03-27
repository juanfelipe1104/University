#include "clientManager.h"


void clientManager::atiendeCliente(int clientId){
	personaFuncs tipoMsg;
	std::vector<unsigned char> buffer;
	//repetir
	do{
		//recibir mensaje
		recvMSG(clientId, buffer);
		//desempaquetar tipo de mensaje
		tipoMsg=unpack<personaFuncs>(buffer);
			//si tipo mensaje
		switch(tipoMsg){
			case PersonaF:{
					//constructor defecto
					Persona p;
					
					//almacenar nueva persona
					clients[clientId]=p;
					buffer.clear();
					pack(buffer,ackMSG);
					
				}break;
			case PersonaParamsF:{

					string nombre;
					int edad;
					
					nombre.resize(unpack<int>(buffer));
					unpackv<char>(buffer,(char*)nombre.data(),nombre.size());
					edad=unpack<int>(buffer);
					
					Persona p(nombre,edad);
					
					//almacenar nueva persona
					clients[clientId]=p;
					buffer.clear();
					pack(buffer,ackMSG);					
				}break;
			case PersonaDF:{
					clients.erase(clientId);
					buffer.clear();
					pack(buffer,ackMSG);					
				}break;
			case sendMSGF:{
				string msg;
				msg.resize(unpack<int>(buffer));
				unpackv<char>(buffer,(char*)msg.data(),msg.size());
				
				if(log)
					log->addMessage(clients[clientId].getNombre(),msg);
				
				buffer.clear();
				pack(buffer,ackMSG);
			}break;
			case recvMSGF:{
				if(log){
					std::vector<std::string> msgs = log->getMessages();
					//pack ack
					pack(buffer,(personaFuncs)ackMSG);
					//pack numero mensajes
					pack(buffer,(int)msgs.size());
					//pack mensajes
					for(auto &m: msgs){
						pack(buffer,(int)m.size());
						packv(buffer,(char*)m.data(),m.size());
					}
				}else{
					//pack ack
					pack(buffer,(personaFuncs)ackMSG);
					//pack numero mensajes
					pack(buffer,(int)0);					
				}
			}break;
			case setNombreF:{
				string nombre;
				nombre.resize(unpack<int>(buffer));
				unpackv<char>(buffer,(char*)nombre.data(),nombre.size());
				
				clients[clientId].setNombre(nombre);
				buffer.clear();
				pack(buffer,ackMSG);				
				
			}break;
			case setEdadF:{
				
				clients[clientId].setEdad(unpack<int>(buffer));
				buffer.clear();
				pack(buffer,ackMSG);			
	
				}break;
			case getNombreF:{
				//invocar funcion
				string nombre=clients[clientId].getNombre();
				//pack ack
				pack(buffer,(personaFuncs)ackMSG);
				//pack nombre
				pack(buffer,(int)nombre.size());
				packv(buffer, (char*)nombre.data(),nombre.size());
				
				}break;
			case getEdadF:{
				//invocar funcion
				//pack ack
				pack(buffer,(personaFuncs)ackMSG);
				//pack nombre
				pack(buffer,(int)clients[clientId].getEdad());
			}break;
			
			default:{
				std::cout<<"ERROR: tipo de mensaje no valido\n";
			}break;
		}
		
		sendMSG(clientId,buffer);
	//mientras no tipo closed
	}while(tipoMsg!=PersonaDF);
	closeConnection(clientId);
}