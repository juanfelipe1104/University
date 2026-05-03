// src/app.js
import express from 'express';
import helmet from 'helmet';
import path from 'node:path';
import router from './routes/routes.js';
import { logger } from './middleware/logger.js';
import { notFoundHandler, errorHandler } from './middleware/errorHandler.js';
import swaggerUi from 'swagger-ui-express';
import swaggerSpecs from './docs/swagger.js';
import { io } from './socket/server.js';

const app = express();

app.set('io', io);

app.use(express.json());

app.use(helmet());

app.use(logger);

app.use(express.static('public'));

app.use('/assets', express.static(path.join(import.meta.dirname, 'public')));

app.use(router);

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpecs));

app.use(notFoundHandler);

app.use(errorHandler);

export default app;