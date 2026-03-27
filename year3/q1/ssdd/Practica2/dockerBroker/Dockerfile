FROM ubuntu:20.04
RUN apt update
RUN apt install software-properties-common -y
RUN apt update
WORKDIR /app
COPY brokerFileManager /app/
EXPOSE 32002

# Entrypoint fija el ejecutable
ENTRYPOINT ["./brokerFileManager"]
