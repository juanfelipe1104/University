# Práctica 5 – Sistema de Mensajería Distribuido  
**MongoDB - Redis - Neo4j**

## 1. Descripción general

Esta práctica implementa un sistema de mensajería distribuido utilizando tres bases de datos con diferentes roles:

- **Neo4j**: grafo de usuarios y relaciones de mensajería.
- **Redis**: sistema de colas, una cola por relación entre usuarios.
- **MongoDB**: almacenamiento persistente del histórico de mensajes y snapshots del sistema.

El sistema permite:
- Enviar mensajes entre usuarios conectados.
- Consumir mensajes desde colas Redis y persistirlos en MongoDB.
- Realizar consultas avanzadas en Neo4j y MongoDB.
- Crear y restaurar snapshots que capturan el estado completo del sistema.

## 2. Requisitos

### Software
- Python **3.10 o superior**
- Neo4j (Community Edition)
- Redis
- MongoDB

Todos los notebooks incluyen los comandos para instalar las librerías requeridas. Se deberá reiniciar el notebook después de la instalación de la librería requerida

## 3. Configuración del entorno
Crear o editar el archivo .env.local suministrado en la carpeta messaging_system
```
# Neo4j
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# Redis
REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_DB="0"

# MongoDB
MONGO_URI="mongodb://localhost:27017"
MONGO_DB="messaging_system"
```

## 4. Estructura del proyecto
```
messaging_system/
│
├── apis/
│   ├── neo4j_api.py
│   ├── redis_api.py
│   ├── mongodb_api.py
│   ├── messageData.py
│   ├── userData.py
│   ├── relationData.py
|   └── messaging_service.py
|   └── snapshot_service.py
│   └── __init__.py
│
├── notebooks/
│   ├── neo4j.ipynb
│   ├── redis.ipynb
│   ├── mongo.ipynb
│   └── messaging_service.ipynb
│
├── .env.local
└── README.md
```

## 5. Orden de ejecución
Todos los notebooks son independientes uno del otro. El notebook principal que engloba todo el proyecto es **messaging_service.ipynb**. neo4j, redis, mongo notebooks prueban los métodos concretos de cada api correspondiente pero no guardan relación entre sí.