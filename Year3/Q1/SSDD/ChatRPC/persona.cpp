#include "persona.h"

Persona::Persona():nombre(""),edad(0){}
Persona::Persona(std::string nombre, int edad){
    this->nombre=nombre;
    this->edad=edad;
}
Persona::~Persona(){}
	
void Persona::setNombre(std::string nombre){this->nombre=nombre;}
void Persona::setEdad(int edad){this->edad=edad;}
std::string Persona::getNombre(){return nombre;}
int Persona::getEdad(){return edad;}

void Persona::enviarMensaje(std::string msg){
    std::cout<<"[Persona] "<<nombre<<": "<<msg<<std::endl;
}

std::vector<std::string> Persona::getMensajes(){
    std::vector<std::string> msgs;
    msgs.push_back("Mensaje 1 de " + nombre);
    msgs.push_back("Mensaje 2 de " + nombre);
    return msgs;
}
