#pragma once
#include "utils.h"

typedef enum
{
    RegisterF,
    UnregisterF,
    ListServersF,
    GetServerF,
    ackMSGF
} brokerFuncs;

class BrokerManager
{
public:
    static inline std::mutex mtx;
    static inline std::map<std::string, details> servers;
    static inline details brokerDetails = {"127.0.0.1", 5050}; // Amazon: 98.86.76.36
    static std::string key(std::string &ip, int port);
    static void registerServer(std::string &ip, int port);
    static void unregisterServer(std::string &ip, int port);
    static std::vector<details> listServers();
    static details getServerDetails();
};