/*
import http from 'node:http';

const PORT = process.env.PORT;

const URLS = process.env.URLS ? process.env.URLS.split(',') : [];

async function oldPost(req, res) {
    let body = '';
    req.on('data', (chunk) => {
        body += chunk;
    });
    req.on('end', () => {
        console.log('Cuerpo de la petición:', body);
        res.writeHead(201);
        res.end(body);
    });
}

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
    console.log("Recibida una petición");
    if (req.method === 'GET') {
        if (!URLS.includes(`http://localhost:${PORT}${req.url}`)) {
            res.writeHead(404);
            res.end('{message:"No encontrado"}');
            return;
        }
        res.writeHead(200);
        res.end('{message:"Hola mundo"}');
    }
    else if (req.method === 'POST') {
        processPost(req, res);
    }
})

server.listen(PORT, () => {
    console.log(`Escuchando en el puerto ${PORT}`);
})


server.on('error', (error) => {
    if (error.code === 'EADDRINUSE') {
        console.log('Error del servidor:', error);
        server.listen(0, () => {
            console.log(`Escuchando en el puerto ${server.address().port}`);
        });
    }
});
*/
/*
import { EventEmitter, once } from 'node:events';

const emisor = new EventEmitter();

async function esperarEvento() {
    console.log('Esperando evento...');
    const [mensaje] = await once(emisor, 'evento');
    console.log('Evento recibido con mensaje:', mensaje);
}

esperarEvento();

setTimeout(() => {
    emisor.emit('evento', '¡Hola desde el evento!');
}, 2000);

console.log('Programa finalizado');
*/
/*
import { EventEmitter, once } from 'node:events';

const emisor = new EventEmitter();

async function esperarEventoConTimeout() {
    const controlador = new AbortController();
    const { signal } = controlador;

    setTimeout(() => {controlador.abort();}, 3000);

    try {
        const [mensaje] = await once(emisor, 'evento', { signal });
        console.log('Evento recibido con mensaje:', mensaje);
    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Tiempo de espera agotado');
        }
    }
}

esperarEventoConTimeout();

setTimeout(() => { emisor.emit('evento', '¡Hola desde el evento!'); }, 3500);

*/

import { PizzaShop } from './pizzaExpress.js';

const pizzaShop = new PizzaShop();

pizzaShop.on('order:received', (order) => {
    console.log(`Order ${order.id} received for ${order.pizza} by ${order.customer}`);
});

pizzaShop.on('order:prepared', (order) => {
    console.log(`Order ${order.id} prepared`);
});

pizzaShop.on('order:baked', (order) => {
    console.log(`Order ${order.id} baked`);
});

pizzaShop.on('order:ready', (order) => {
    console.log(`Order ${order.id} is ready for pickup`);
});

pizzaShop.on('order:failed', (order) => {
    console.log(`Order ${order.id} has failed`);
});

pizzaShop.on('shop:stats', (stats) => {
    console.log(`Stats: ${JSON.stringify(stats)}`);
})

const pedido1 = pizzaShop.processOrder(1, 'pizza:jamon', 'Juan');

const pedido2 = pizzaShop.processOrder(2, 'pizza:pepperoni', 'Daniel');