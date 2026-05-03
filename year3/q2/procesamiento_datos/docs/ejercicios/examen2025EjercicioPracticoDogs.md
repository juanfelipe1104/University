En este ejercicio, vamos a utilizar, por un lado, datos desestructurados sobre perros registrados en un refugio animal y, por otro, datos estructurados con información sobre razas de perros. Posteriormente y, después de algunas transformaciones, se deberán volcar ciertos datos sobre un sink de Streaming (topic de Kafka). El comando o código utilizado en cada paso debe ser incluído en formato texto en el campo de respuesta de la pregunta de Blackboard como solución final:

- Paso 1: Descargar los ficheros de datos (No requiere incluir los comandos en la solución final) y explora el contenido del fichero csv (por ejemplo, con el comando head)

```bash
wget -P /root/ https://gist.githubusercontent.com/mafernandez-stratio/f79505ec0d69199f8e80c93a6005a8aa/raw/43eb90cff53ec9e3f7cb6daeda5b305ef42e389a/dogs_shelter.txt

wget -P /root/ https://gist.githubusercontent.com/mafernandez-stratio/1402d7d2fdd900707b2f9997441d8b42/raw/7bcd6fa2e4aee41438956139cc9380b754337730/dogs_breeds.csv
```

- Paso 2: Arranca HDFS y copia el fichero dogs_shelter.txt a la ruta /data/dogs/ de HDFS y el fichero dogs_breeds.csv a la ruta /data/breeds/

```bash
bin/hdfs dfs -mkdir -p /data/dogs
bin/hdfs dfs -mkdir -p /data/breeds
bin/hdfs dfs -put /root/dogs_shelter.txt /data/dogs
bin/hdfs dfs -put /root/dogs_breeds.csv /data/breeds
```

- Paso 3: Arranca la shell de Spark con la dependencia del conector de Kafka (--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3) y crea una tabla (NO debe ser una tabla temporal) con nombre dogbreeds con los datos sobre razas (breeds) de perros albergados en HDFS (incluye las opciones del datasource de csv que estimes oportunas tras haber realizado la exploración del fichero en el paso anterior):

```bash
bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7
```

```scala
import spark.implicits._
import org.apache.spark.sql._

spark.sql("CREATE TABLE dogbreeds USING csv OPTIONS (path 'hdfs://hdfs:8020/data/breeds/dogs_breeds.csv', header 'true', inferSchema 'true')")
```

- Paso 4: Genera un RDD (dogsRDD) que cargue las líneas de los datos sobre los perros del refugio (shelter) albergados en HDFS

```scala
val dogsRDD = sc.textFile("hdfs://hdfs:8020/data/dogs/dogs_shelter.txt")
```

- Paso 5: Convierte este RDD dogsRDD en un Dataframe (dogsDF) con la siguiente estructura:

scala> dogsDF.printSchema
root
 |-- id: integer (nullable = false)
 |-- name: string (nullable = true)
 |-- raza: string (nullable = true)
 |-- pais_nacimiento: string (nullable = true)
 |-- edad: integer (nullable = false)
 |-- peso: integer (nullable = false)
 |-- altura_cms: integer (nullable = false)

NOTA 1: Ten en cuenta que la primera línea de dogs_shelter.txt es una cabecera con metadatos, por tanto, esta primera línea no contiene datos

NOTA 2: Si tenemos la línea: "1&&&1:RHUBARB&&&1:Cheagle&&&1:Guam&&&1:12&&&1:2&&&1:43", nuestro Dataframe dogsDF contendrá una fila donde -> id=1, name="RHUBARB", raza="Cheagle", pais_nacimiento="Guam", edad=12, peso=2, altura_cms=43

```scala
case class Dog(id: Int, name: String, raza: String, pais_nacimiento: String, edad: Int, peso: Int, altura_cms: Int)

val dogsShelterRDD = dogsRDD.filter(!_.startsWith("id"))

val dogsDF = dogsShelterRDD.map(_.split(":").map(_.split("&&&")(0))).map(row => Dog(row(0).toInt, row(1), row(2), row(3), row(4).toInt, row(5).toInt, row(6).toInt)).toDF
```

- Paso 6: Registra el Dataframe dogsDF como una tabla temporal con el nombre dogs_shelter

```scala
dogsDF.createOrReplaceTempView("dogs_shelter")
```

- Paso 7: Crea una tabla (NO debe ser una tabla temporal) con el nombre dogs que sea el resultado de realizar una operación JOIN entre las tablas dogbreeds (utilizando la columna Breed_Name) y dogs_shelter (utilizando la columna raza)

```scala
spark.sql("CREATE TABLE dogs AS SELECT DISTINCT * FROM dogbreeds db JOIN dogs_shelter ds ON db.Breed_Name = ds.raza")
```

- Paso 8: ¿Cuál es la media de la columna Easy_To_Train de la tabla dogs?

```scala
spark.sql("SELECT AVG(Easy_To_Train) AS mediaEntrenar FROM dogs").show()
```

- Paso 9: ¿Cuántos perros hay de cada tamaño (Dog_Size) en función de su raza (Breed_Name/raza) en la tabla dogs?

```scala
spark.sql("SELECT Breed_Name, Dog_Size, COUNT(*) AS amount FROM dogs GROUP BY Breed_Name, Dog_Size ORDER BY Breed_Name").show()
```

- Paso 10: ¿Cuál es la edad máxima (edad) por cada país de nacimiento (pais_nacimiento) de los perros que pertenecen a una raza cuya inteligencia (Intelligence) es mayor que 4?

```scala
spark.sql("SELECT pais_nacimiento, MAX(edad) AS edad_maxima FROM dogs WHERE Intelligence > 4 GROUP BY pais_nacimiento ORDER BY pais_nacimiento").show()
```

- Paso 11: Inicia un servicio de Kafka (es decir, levantar un Broker de Kafka), crea el topic dogs y, posteriormente, una consola consumidor de Kafka del topic dogs, que pertenezca al consumer group grupo1, que imprima la clave de cada mensaje y que utilice los caracteres --> como separador entre la clave y el valor

```bash
bin/kafka-topics --create --topic dogs --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic dogs --group grupo1 --property print.key=true --property key.separator="-->" --from-beginning
```

- Paso 12: Responde a la siguiente pregunta volcando los datos resultantes sobre el topic dogs: ¿Cuales son los nombres y su potencial a ganar peso (Potential_For_Weight_Gain) de los perros cuya altura real (altura_cms) es mayor que la altura media de su raza (Avg_Height_cm)?
NOTA: Utiliza el datasource "kafka" y su interfaz batch (dataframe.write)

```scala
val dogsToKafkaDF = spark.sql("SELECT CAST(name AS STRING) AS key, CAST(Potential_For_Weight_Gain AS STRING) AS value FROM dogs WHERE altura_cms > Avg_Height_cm")

dogsToKafkaDF.write.format("kafka").option("kafka.bootstrap.servers", "confluent:9092").option("topic", "dogs").save()
```
