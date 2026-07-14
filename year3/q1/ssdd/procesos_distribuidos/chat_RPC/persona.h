#pragma once
#include <string>
#include <vector>
#include <iostream>

class Persona{
		private:
			std::string nombre;
			int edad;
		public:
			Persona();
			Persona(std::string nombre, int edad);
			~Persona();
			void setNombre(std::string nombre);
			void setEdad(int edad);
			void enviarMensaje(std::string msg);
			std::string getNombre();
			int getEdad();
			std::vector<std::string> getMensajes();

};
