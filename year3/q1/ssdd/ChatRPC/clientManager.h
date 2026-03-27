#pragma once
#include "utils.h"
#include "persona.h"
#include "log.h"
using namespace std;
typedef enum{

	PersonaF,//constructor defecto
	PersonaParamsF,//constructor parametros
	PersonaDF,//destructor
	setNombreF,
	setEdadF,
	getNombreF,
	getEdadF,
	sendMSGF, //enviar mensaje
	recvMSGF, //recibir mensaje
	ackMSG
}personaFuncs;

class clientManager{

		public:
		
			static inline map<int, Persona> clients;
			static inline map<Persona*,connection_t > connectionIds;
			
			static inline Log* log = nullptr;
			
			static inline bool salir=false;			
			static void atiendeCliente(int clientId);
};