#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <mutex>

class Log{
    private:
        std::mutex mtx;
        std::vector<std::string> messages;
    public:
        void addMessage(std::string author, std::string message);
        std::vector<std::string> getMessages();
};