package com.juan.procesamientodatos
package sparkClase.sql

import sparkClase.SparkProvider

import org.apache.spark.sql.Row
import org.apache.spark.sql.types._

object df_example extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc

  import spark.implicits._

  // 1. CREATING A DF IN SPARK
  val data = Seq(
    ("Juan", "ciencias", 7.2),
    ("Maria", "matematicas", 8.7),
    ("Pedro", "historia", 3.4),
    ("Rosa", "ciencias", 6.8),
    ("Julia", "historia", 7.6),
    ("Luis", "matematicas", 9.5)
  )

  // 1.1. Creating a dataframe by using toDF()
  val mydf = data.toDF("alumno", "asignatura", "calificacion")

  // 1.2. Creating a dataframe by defining its structure and using the method createDataFrame
  val schema = List(
    StructField("alumno", StringType, true),
    StructField("asignatura", StringType, true),
    StructField("calificacion", DoubleType, true)
  )

  // Defining a sequence of Rows; once it is parallelized, a RDD of Rows or RDD[Row] is obtained. This is in essence the structure of a dataframe
  val data_rows = data.map { case (alumno, asignatura, calificacion) =>
    Row(alumno, asignatura, calificacion)
  }
  val anotherdf = spark.createDataFrame(sc.parallelize(data_rows), StructType(schema))

  data.toDF("alumno", "asignatura", "calificacion")

  // 1.3. Read data from csv file
  spark.read.format("csv").load("/src/main/scala/files/winequality-red-white.txt").show()
  spark.read.csv("/src/main/scala/files/winequality-red-white.txt").show()
  val tmp1df = spark.read.format("csv").option("header", "true").load("/src/main/scala/files/winequality-red-white.txt")

  // Problem? Delimiter is not a comma, but a pipe --> Specify "delimiter" option
  val tmp2df = spark.read.format("csv").option("header", "true").option("delimiter", "|").load("/src/main/scala/files/winequality-red-white.txt")

  // Problem? All the columns as string, but they represent figures. --> Specify "inferSchema" option
  val winesdf = spark.read.format("csv").option("header", "true").option("delimiter", "|").option("inferSchema", "true").load("/src/main/scala/files/winequality-red-white.txt")

  // 2. DF STRUCTURE (METADATA)
  // 2.1. Método printSchema
  winesdf.printSchema

  // 2.2. Método dtypes
  winesdf.dtypes

  // 2.3. Método columns
  winesdf.columns

  // 3. FROM DATAFRAME TO RDD
  val myrdd = mydf.rdd.map(r => (r.getAs[String]("alumno"), r.getAs[Double]("calificacion")))
  myrdd.first()

  // 4. INITIAL EXPLORATION OF THE DATAFRAME
  // Inspeccionamos su contenido
  winesdf.show()
  winesdf.show(10)
  winesdf.show(10, truncate = false)

  // Exploramos con mayor detenimiento algunas variables
  winesdf.describe("fixed_acidity", "density").show

  // Número de elementos en el dataframe
  winesdf.count()

  // Número de graduaciones de alcohol distintas que nos encontramos
  winesdf.select("alcohol").distinct().count

  // 5. SOME INITIAL QUERIES
  // 5.1. Creamos una vista temporal de la tabla que desaparecerá al cerrar la sesión

  winesdf.createGlobalTempView("wines")

  // 5.2. Tras registrar la tabla, podemos lanzar queries SQL mediante el método "sql" del objeto SparkSession
  spark.sql("select fixed_acidity, density from global_temp.wines").show

  // 5.3. Esta misma query podemos llevarla a cabo mediante la API de Spark
  winesdf.select("fixed_acidity", "density").show
}
