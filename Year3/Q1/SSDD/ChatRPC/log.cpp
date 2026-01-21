#include "log.h"

void Log::addMessage(std::string author, std::string message){
    this->mtx.lock();
    this->messages.push_back(author + ": " + message);
    this->mtx.unlock();
}

std::vector<std::string> Log::getMessages(){
    this->mtx.lock();
    std::vector<std::string> msgs = this->messages;
    this->mtx.unlock();
    return msgs;
}