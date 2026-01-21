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
