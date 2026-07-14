#include "brokermanager.h"

// Key para mapear el servidor con sus datos
std::string BrokerManager::key(std::string &ip, int port)
{
    return ip + ":" + std::to_string(port);
}

void BrokerManager::registerServer(std::string &ip, int port)
{
    BrokerManager::mtx.lock();
    BrokerManager::servers[key(ip, port)] = details{ip = ip, port = port};
    BrokerManager::mtx.unlock();
}

void BrokerManager::unregisterServer(std::string &ip, int port)
{
    BrokerManager::mtx.lock();
    BrokerManager::servers.erase(BrokerManager::key(ip, port));
    BrokerManager::mtx.unlock();
}

std::vector<details> BrokerManager::listServers(){
    std::vector<details> serversList;
    BrokerManager::mtx.lock();
    serversList.reserve(BrokerManager::servers.size());
    for(auto &kv : servers){
        serversList.push_back(kv.second);
    }
    BrokerManager::mtx.unlock();
    return serversList;
}

details BrokerManager::getServerDetails()
{
    return BrokerManager::servers.begin()->second;
}

details BrokerManager::getServerDetails(){
    details serverDetails = {BrokerManager::ip, BrokerManager::port};
    return serverDetails;
}