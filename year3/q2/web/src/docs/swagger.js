import swaggerJsdoc from 'swagger-jsdoc';

const options = {
    definition: {
        openapi: '3.0.3',
        info: {
            title: 'API de Notes - Express con Swagger',
            version: '1.0.0',
            description: 'API REST documentada con Swagger',
            license: {
                name: 'MIT',
                url: 'https://spdx.org/licenses/MIT.html'
            },
            contact: {
                name: 'Juan Rodriguez',
                email: 'tu@email.com'
            }
        },
        servers: [
            {
                url: 'http://localhost:3000',
                description: 'Servidor de desarrollo'
            }
        ],
        components: {
            securitySchemes: {
                bearerAuth: {
                    type: 'http',
                    scheme: 'bearer',
                    bearerFormat: 'JWT'
                }
            },
            schemas: {
                User: {
                    type: 'object',
                    required: ['name', 'email', 'password'],
                    properties: {
                        name: { type: 'string', example: 'Juan Pérez' },
                        email: { type: 'string', format: 'email', example: 'juan@ejemplo.com' },
                        password: { type: 'string', format: 'password', example: 'MiPassword123' },
                        age: { type: 'integer', example: 25 },
                        role: { type: 'string', enum: ['user', 'admin'], default: 'user' }
                    }
                },
                Error: {
                    type: 'object',
                    properties: {
                        error: { type: 'boolean', example: true },
                        message: { type: 'string', example: 'Error message' }
                    }
                }
            }
        }
    },
    apis: ['./src/routes/*.js']
};

const swaggerSpecs = swaggerJsdoc(options);

export default swaggerSpecs;