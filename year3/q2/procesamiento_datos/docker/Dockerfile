FROM spark:3.5.7-scala2.12-java17-r-ubuntu

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-server openssh-client git maven netcat vim iproute2 \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /var/run/sshd

# SSH: permitir root por contraseña (solo prácticas)
RUN sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
 && sed -i 's/^#\?PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config \
 && echo "root:root" | chpasswd

# Preparar claves del host (evita que sshd falle al arrancar)
RUN ssh-keygen -A

# Preparar SSH sin contraseña para root (para scripts start-workers.sh)
RUN mkdir -p /root/.ssh \
 && ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa \
 && cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys \
 && chmod 700 /root/.ssh \
 && chmod 600 /root/.ssh/authorized_keys \
 && printf "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile=/dev/null\n" > /root/.ssh/config \
 && chmod 600 /root/.ssh/config

RUN echo "export JAVA_HOME=/opt/java/openjdk" >> /opt/spark/bin/load-spark-env.sh \
 && echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /opt/spark/bin/load-spark-env.sh 

# Clonar repositorio dentro de Spark
RUN git clone https://github.com/mafernandez-stratio/spark-very-basic-server.git /opt/spark/work-dir/spark-very-basic-server

RUN cd /opt/spark/work-dir/spark-very-basic-server/ && mvn clean package && mvn clean compile assembly:single

RUN apt-get install -y --no-install-recommends wget curl

ENV SPARK_DAEMON_JAVA_OPTS="--add-exports=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED"
ENV SPARK_DRIVER_EXTRAJAVAOPTIONS="--add-exports=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED"
ENV SPARK_EXECUTOR_EXTRAJAVAOPTIONS="--add-exports=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED"
ENV SPARK_MASTER_REST_ENABLED=true
ENV SPARK_MASTER_OPTS="-Dspark.master.rest.enabled=true"

RUN echo "spark.history.fs.logDirectory hdfs://hdfs:8020/shared/spark-logs" > /opt/spark/work-dir/history-server.conf

RUN wget -q -P /opt/spark/work-dir/ https://gist.githubusercontent.com/mafernandez-stratio/4d65c9ad88b40ca4cbe9f9b7da67d8f7/raw/aa08fee35b3d687990c8bd80192b200f7b148780/winequality-red-white.txt

RUN wget -q -P /opt/spark/work-dir/ https://gist.githubusercontent.com/mafernandez-stratio/9dd41b7fca11d953901b8f5a89b36176/raw/9f7a3ca4acac0817cafdd649b6691acb26e241da/fruits.json
RUN wget -q -P /opt/spark/work-dir/ https://gist.githubusercontent.com/mafernandez-stratio/a694fe539e4e1b14d151a1ede0339f1d/raw/2056783dfcc057f43e880faabdef63781bf8b193/access.log
RUN wget -q -P /opt/spark/work-dir/ https://gist.githubusercontent.com/mafernandez-stratio/c1e092f9a0aeb073a35200f4555cea1d/raw/effba761c6bb0a5a86f6bb2171fbfbf95e3509de/emails.txt
RUN wget -q -P /opt/spark/work-dir/ https://gist.githubusercontent.com/mafernandez-stratio/6486eacb387350d8e9b2d5890777dd3a/raw/b83478b6a0471caa4c4abee20c08d2401e380779/winemag.csv
RUN wget -q -P /opt/spark/work-dir/ https://gist.githubusercontent.com/mafernandez-stratio/c97926996ca458e66600215bb47f93b6/raw/9f557a7955c130dda82b640ff512d4f5735e763a/winemag_special_format.csv
RUN wget -q -P /opt/spark/work-dir/ https://gist.githubusercontent.com/mafernandez-stratio/5cba89aeea095f6afaf4f241b89deec3/raw/14e2fa593c13eef6f3453ced67bc40dafa76dcc1/earthquakes_2024.json
RUN wget -q -P /opt/spark/work-dir/ https://repo1.maven.org/maven2/org/postgresql/postgresql/42.3.7/postgresql-42.3.7.jar

# Establecer directorio de trabajo
WORKDIR /opt/spark

EXPOSE 22

# Script de arranque
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Por defecto abre una shell (puedes cambiarlo por spark master/worker)
CMD ["bash"]