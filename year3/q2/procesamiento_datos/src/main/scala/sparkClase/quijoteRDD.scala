package com.juan.procesamientodatos
package sparkClase

object quijoteRDD extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  val quijoteRDD = sc.textFile("src/main/scala/files/pg2000.txt")

  // 1. Preparación
  println(s"Particiones iniciales: ${quijoteRDD.getNumPartitions}")

  // 2. ¿En cuántas líneas aparece la palabra "molino"?
  val lineasConMolino = quijoteRDD.map(_.toLowerCase).filter(linea => linea.contains("molino")).count()
  println(s"Líneas donde aparece 'molino': $lineasConMolino")

  // 3. ¿Cuántas palabras distintas aparecen en el texto?
  val palabrasDistintas = quijoteRDD.flatMap(_.split("\\s+")).map(_.replaceAll("""[^\p{L}\p{N}]""", "").toLowerCase).filter(_.nonEmpty).distinct().count()
  println(s"Palabras distintas: $palabrasDistintas")

  // 4. ¿Cuáles son las 10 palabras, de más de 3 letras, más repetidas y cuántas veces?
  val top10Palabras = quijoteRDD.flatMap(_.split("\\s+")).map(_.replaceAll("""[^\p{L}\p{N}]""", "").toLowerCase).filter(palabra => palabra.length > 3).map(palabra => (palabra, 1)).reduceByKey(_ + _).map { case (palabra, frecuencia) => (frecuencia, palabra) }.sortByKey(ascending = false).take(10)
  println("Top 10 palabras de más de 3 letras:")
  top10Palabras.foreach(println)

  // 5. ¿Cuántas veces aparece la palabra “hidalgo”?
  val aparicionesHidalgo = quijoteRDD.flatMap(_.split("\\s+")).map(_.replaceAll("""[^\p{L}\p{N}]""", "").toLowerCase).filter(_ == "hidalgo").count()
  println(s"Apariciones de 'hidalgo': $aparicionesHidalgo")

  // 6. ¿Cuántas líneas tiene el texto?
  val numeroLineas = quijoteRDD.count()
  println(s"Número de líneas: $numeroLineas")

  // 7. ¿Cuántas líneas tienen más de 20 caracteres?
  val lineasMasDe20 = quijoteRDD.filter(_.length > 20).count()
  println(s"Líneas con más de 20 caracteres: $lineasMasDe20")

  // 8. ¿Cuál es la línea más larga y con cuántos caracteres?
  val lineaMasLarga = quijoteRDD.map(linea => (linea.length, linea)).sortByKey(ascending = false).take(1)
  println("Línea más larga:")
  lineaMasLarga.foreach(println)
  spark.stop()
}
