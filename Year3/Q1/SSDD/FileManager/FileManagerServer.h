#pragma once
#include "utils.h"
#include "filemanager.h"
using namespace std;

typedef enum
{
    FileManagerF,
    FileManagerDF,
    listFilesF,
    readFileF,
    writeFileF,
    ackMSG
} fileFuncs;

class FileManagerServer
{
public:
    static inline map<int, FileManager> clients;
    static inline map<FileManager *, connection_t> connectionIds;

    static void attendClient(int clientId);
};