import http from 'node:http';

const PORT = process.env.PORT;

async function processPost(req, res) {
    let body = '';
    for await (const chunk of req) {
        body += chunk;
    }
    console.log('Cuerpo de la petición:', body);
    res.writeHead(201);
    res.end(body);
}

const server = http.createServer((req, res) => {
    if (req.method === 'GET') {
        handleGet(req, res);
    }
})

function handleGet(req, res) {
    if(req.url === '/'){
        res.writeHead(200);
        res.end('Bienvenido a la API');
    }
    else if(req.url === '/health'){
        res.writeHead(200);
        res.end(`{status:"ok", timestamp:"${new Date()}"}`);
    }
    else{
        res.writeHead(404);
        res.end('{message:"No encontrado"}');
    }
}

server.listen(PORT, () => {
    console.log(`Escuchando en el puerto ${PORT}`);
})


server.on('error', (error) => {
    if (error.code === 'EADDRINUSE') {
        server.listen(0, () => {
            console.log(`Escuchando en el puerto ${server.address().port}`);
        });
    }
});