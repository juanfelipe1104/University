import { EventEmitter } from 'node:events';
import { setTimeout } from 'node:timers/promises';

export class PizzaShop extends EventEmitter {
    constructor() {
        super();
        this.orders = []
    }
    async processOrder(id, pizza, customer) {
        const order = { id, pizza, customer, status: 'pending', timestamps: {} };
        Promise.allSettled([
            this.#receiveOrder(order),
            this.#prepareOrder(order),
            this.#bakeOrder(order),
            this.#readyOrder(order),
            this.#printStats(order)
        ]);
        this.orders.push(order);
    }
    async #receiveOrder(order){
        if (this.#canFail()){
            this.#failOrder(order);
            return;
        }
        order.status = 'received';
        order.timestamps.received = new Date();
        this.emit('order:received', order);
    }
    async #prepareOrder(order){
        if (this.#canFail()){timestamps
            this.#failOrder(order);
            return;
        }
        await setTimeout(this.#randomDelay(1000, 3000));
        order.status = 'prepared';
        order.timestamps.preparing = new Date();
        this.emit('order:prepared', order);
    }
    async #bakeOrder(order){
        if (this.#canFail()){
            this.#failOrder(order);
            return;
        }
        await setTimeout(this.#randomDelay(2000, 4000));
        order.status = 'baked';
        order.timestamps.baking = new Date();
        this.emit('order:baked', order);
    }
    async #readyOrder(order){
        if (this.#canFail()){
            this.#failOrder(order);
            return;
        }
        order.status = 'ready';
        order.timestamps.ready = new Date();
        this.emit('order:ready', order);
    }
    async #printStats(order){
        setInterval(() => {
            this.emit('shop:stats', order.timestamps);
        }, 2000);
    }
    #canFail(){
        return Math.random() < 0.1;
    }
    #failOrder(order){
        order.status = 'failed';
        this.emit('order:failed', order);
    }
    #randomDelay(min, max){
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
}

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