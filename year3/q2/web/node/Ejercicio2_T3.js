import http from 'node:http';

const PORT = process.env.PORT;
const cursos = [
    { id: 1, titulo: 'JavaScript Básico', nivel: 'basico', vistas: 1500 },
    { id: 2, titulo: 'Node.js Intermedio', nivel: 'intermedio', vistas: 980 },
    { id: 3, titulo: 'Express Avanzado', nivel: 'avanzado', vistas: 750 }
];

const server = http.createServer((req, res) => {
    if (req.method === 'GET') {
        handleGet(req, res);
    }
    else if (req.method === 'POST') {
        handlePost(req, res);
    }
    else if (req.method === 'PUT') {
        handlePut(req, res);
    }
    else if (req.method === 'DELETE') {
        handleDelete(req, res);
    }
})

function handleGet(req, res) {
    if(req.url === '/api/cursos'){
        res.writeHead(200);
        res.end(JSON.stringify(cursos));
    }
    else if(req.url.startsWith('/api/cursos/')){
        const id = parseInt(req.url.split('/')[4]);
        const curso = cursos.find(c => c.id === id);
        if(curso){
            res.writeHead(200);
            res.end(JSON.stringify(curso));
        } else {
            res.writeHead(404);
            res.end('{message:"Curso no encontrado"}');
        }
    }
    else if(req.url.startsWith('/api/cursos?')){
        const nivel = req.url.searchParams.get('nivel');
        if(nivel){
            const cursosBasicos = cursos.filter(c => c.nivel === nivel);
            res.writeHead(200);
            res.end(JSON.stringify(cursosBasicos));
        }
        else{
            res.writeHead(400);
            res.end('{message:"Parámetro no encontrado"}');
        }
    }
    else{
        res.writeHead(404);
        res.end('{message:"No encontrado"}');
    }
}

function getBody(req){
    let body = '';
    for await (const chunk of req) {
        body += chunk;
    }
    return body;
}

function handlePost(req, res) {
    const body = getBody(req);
    const nuevoCurso = JSON.parse(body);
    nuevoCurso.id = cursos.length + 1;
    cursos.push(nuevoCurso);
    res.writeHead(201);
    res.end(JSON.stringify(nuevoCurso));
}

function handlePut(req, res) {
    const body = getBody(req);
    const cursoActualizado = JSON.parse(body);
    const index = cursos.findIndex(c => c.id === cursoActualizado.id);
    if(index !== -1){
        cursos[index] = cursoActualizado;
        res.writeHead(200);
        res.end(JSON.stringify(cursoActualizado));
    } else {
        res.writeHead(404);
        res.end('{message:"Curso no encontrado"}');
    }
}

function handleDelete(req, res) {
    const id = parseInt(req.url.split('/')[4]);
    const index = cursos.findIndex(c => c.id === id);
    if(index !== -1){
        cursos.splice(index, 1);
        res.writeHead(204);
        res.end();
    } else {
        res.writeHead(404);
        res.end('{message:"Curso no encontrado"}');
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