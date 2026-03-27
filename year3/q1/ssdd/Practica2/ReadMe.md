# Practica 2 (Kubernetes y Docker)

El objetivo de la práctica es implementar la arquitectura distribuida de la práctica 1 mediante el uso de kubernetes y docker. Para ello, se plantea un cluster en kubernetes con dos nodos (uno master, otro slave). En el slave se desplegaran pods para todos los componentes (cliente, server, broker) y cada componente tiene su imagen Docker. El cliente estará en un Pod, el servidor y el broker serán un deployment + service cada uno. Se configura un servidor nfs para persistir los archivos

| Componente            | Función                                            |
| --------------------- | -------------------------------------------------- |
| **clientFileManager** | Aplicación interactiva para el usuario             |
| **brokerFileManager** | Registro de servidores y redirección de peticiones |
| **serverFileManager** | Almacenamiento y gestión de ficheros               |

## Cliente

### Dockerfile client
Imagen docker del cliente
```dockerfile
FROM ubuntu:20.04
RUN apt update
RUN apt install software-properties-common -y
RUN apt update
WORKDIR /app
COPY clientFileManager /app/
```

### Pod Configuration
Archivo yaml con la configuración del pod del cliente
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: client-pod
  namespace: default
spec:
  containers:
    - name: kubernetes-client
      image: docker.io/juanfelipe1104/client:latest
      command: ["/bin/sh", "-c"]
      args: ["sleep 3600"]
```

## Servidor

### Dockerfile server
Imagen docker del servidor
```dockerfile
FROM ubuntu:20.04
RUN apt update
RUN apt install software-properties-common -y
RUN apt update
WORKDIR /app
RUN mkdir -p /app/FileManagerDir
COPY serverFileManager /app/
EXPOSE 32001

# Entrypoint fija el ejecutable
ENTRYPOINT ["./serverFileManager"]

# CMD define valores por defecto teniendo entrypoint (se sobrescriben con args: en Kubernetes)
CMD ["127.0.0.1", "32002", "127.0.0.1", "32001"]
```

### Deployment Configuration
Archivo yaml con la configuración del despliegue del servidor
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: server-deployment
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: server
  template:
    metadata:
      labels:
        app: server
    spec:
      containers:
        - name: kubernetes-server
          image: docker.io/juanfelipe1104/server:latest
          ports:
            - containerPort: 32001
          # Variable de entorno para que cada servidor tenga IP diferente
          env:
            - name: OWN_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          command: ["/bin/sh", "-c"]
          args:
            - >
              ./serverFileManager
              $BROKER_SERVICE_SERVICE_HOST
              $BROKER_SERVICE_SERVICE_PORT
              $OWN_IP
              32001
          volumeMounts:
            - name: fm-dir
              mountPath: /app/FileManagerDir
      volumes:
        - name: fm-dir
          nfs:
            server: 172.31.16.89
            path: /export/filemanager
```

### Service Configuration
Archivo yaml con la configuración del servicio del servidor
```yaml
apiVersion: v1
kind: Service
metadata:
  name: server-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: server
  ports:
    - port: 32001
      targetPort: 32001
      nodePort: 32010
  externalTrafficPolicy: Cluster
```

## Broker

### Dockerfile broker
Imagen docker del broker

```dockerfile
FROM ubuntu:20.04
RUN apt update
RUN apt install software-properties-common -y
RUN apt update
WORKDIR /app
RUN mkdir -p /app/FileManagerDir
COPY serverFileManager /app/
EXPOSE 32001

# Entrypoint fija el ejecutable
ENTRYPOINT ["./serverFileManager"]

# CMD define valores por defecto (se sobrescriben con args: en Kubernetes)
CMD ["127.0.0.1", "32002", "127.0.0.1", "32001"]
```

### Deployment Configuration
Archivo yaml con la configuración del despliegue del broker

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: broker-deployment
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: broker
  template:
    metadata:
      labels:
        app: broker
    spec:
      containers:
        - name: kubernetes-broker
          image: docker.io/juanfelipe1104/broker:latest
          ports:
            - containerPort: 32002
```

### Service Configuration
Archivo yaml con la configuración del servicio del broker

```yaml
apiVersion: v1
kind: Service
metadata:
  name: broker-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: broker
  ports:
    - port: 32002
      targetPort: 32002
      nodePort: 32011
  externalTrafficPolicy: Cluster
```