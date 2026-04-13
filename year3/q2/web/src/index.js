// src/index.js
import app from './app.js';
import httpServer from './socket/server.js';
import env from './config/env.js';
import dbConnect from './config/db.js';

const startServer = async () => {
    await dbConnect();

    app.listen(env.PORT, () => {
        console.log(`Servidor ejecutándose en http://localhost:${env.PORT}`);
        console.log(`Entorno: ${env.NODE_ENV}`);
    });

    httpServer.listen(4044, () => {
        console.log('Servidor en http://localhost:4044');
    });
}

await startServer();