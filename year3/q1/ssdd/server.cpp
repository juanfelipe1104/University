#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <cstring>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;

void handle_client(int clientSocket) {
    char buffer[1024];
    while (true) {
        ssize_t n = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
        if (n == 0) {
            // El cliente cerró la conexión
            break;
        }
        if (n < 0) {
            perror("recv");
            break;
        }
        buffer[n] = '\0';
        cout << "Mensaje de cliente: " << buffer << endl;

        // (Opcional) Responder al cliente — eco simple:
        if (send(clientSocket, buffer, n, 0) < 0) {
            perror("send");
            break;
        }
    }
    close(clientSocket);
}

int main() {
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) { perror("socket"); return 1; }

    // Reusar puerto para reiniciar rápido
    int opt = 1;
    if (setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt");
        close(serverSocket);
        return 1;
    }

    sockaddr_in serverAddress{};
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(8080);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    if (bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        perror("bind");
        close(serverSocket);
        return 1;
    }

    if (listen(serverSocket, 16) < 0) {
        perror("listen");
        close(serverSocket);
        return 1;
    }

    cout << "[*] Servidor escuchando en 0.0.0.0:8080\n";

    // Bucle de aceptación: cada cliente se atiende en su propio hilo
    while (true) {
        int clientSocket = accept(serverSocket, nullptr, nullptr);
        if (clientSocket < 0) {
            perror("accept");
            continue;
        }

        // Lanzamos un hilo separado para este cliente
        thread t(handle_client, clientSocket);
        t.detach(); // no bloqueamos el hilo principal
    }

    // (nunca llega aquí en este ejemplo)
    close(serverSocket);
    return 0;
}
