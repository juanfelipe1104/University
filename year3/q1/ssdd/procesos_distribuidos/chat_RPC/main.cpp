#include <iostream>
#include "persona.h"


int main(int argc, char** argv){
	Persona persona;
	std::string nombre;
	int edad = 0, opcion = 0;
	bool salir = false;
	std::cout << "Ingrese su nombre: ";
	std::cin >> nombre;
	persona.setNombre(nombre);
	std::cout << "Ingrese su edad: ";
	std::cin >> edad;
	persona.setEdad(edad);
	while(!salir){
		std::cout << "1. Enviar mensaje\n2. Ver mensajes\n3. Salir\nSeleccione una opcion: ";
		std::cin >> opcion;
		switch(opcion){
			case 1:{
				std::string msg;
				std::cout << "Ingrese su mensaje: ";
				std::cin >> msg;
				persona.enviarMensaje(msg);
			}break;
			case 2:{
				std::vector<std::string> mensajes = persona.getMensajes();
				std::cout << "Mensajes:\n";
				for(std::string &m : mensajes){
					std::cout << m << std::endl;
				}
			}break;
			case 3:
				salir = true;
			break;
			default:
				std::cout << "Opcion no valida\n";
			break;
		}
	}
	return 0;
}

