package com.juan.procesamientodatos
package sparkClase

object transformation_action extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  val rdd_range = sc.parallelize(Range(1, 5000))
  rdd_range.count()
  rdd_range.take(10)
  val rdd_lines = sc.parallelize(Seq("linea 1 Scala", "linea 2 Scala", "linea 3 Spark"))
  val rdd_numbers = sc.parallelize(Seq(1, 2, 3, 3))

  // Map vs FlatMap
  rdd_lines.map(_.split(" ")).collect()
  rdd_lines.flatMap(_.split(" ")).collect()

  // Filter
  rdd_lines.filter(_.contains("Scala")).take(10)

  // FlatMap + Filter
  rdd_lines.flatMap(_.split(" ")).filter(_.contains("Scala")).take(10)
  rdd_lines.filter(_.contains("Scala")).flatMap(_.split(" ")).take(10)
  rdd_lines.cache()
  rdd_lines.unpersist()

  // Distinct
  rdd_numbers.distinct().collect()

  // EJERCICIO 1:
  // Busca en la API de transformaciones de RDDs de Spark
  // https://archive.apache.org/dist/spark/docs/3.3.1/rdd-programming-guide.html#transformations
  // dos métodos que permitan tomar muestras de RDD y aplícalos a rdd_numbers con diferentes parámetros
  // Sample & TakeSample
  rdd_numbers.sample(false, 0.5).collect() // Sin reemplazo
  rdd_numbers.sample(true, 0.5).collect() // Con reemplazo
  rdd_numbers.takeSample(false, 3) // Sin reemplazo
  rdd_numbers.takeSample(true, 3) // Con reemplazo

  // Union
  val rdd_more_numbers = sc.parallelize(Seq(3, 4, 2, 5))
  rdd_numbers.union(rdd_more_numbers).collect()

  // Intersection
  rdd_numbers.intersection(rdd_more_numbers).collect()

  // Subtraction
  rdd_numbers.subtract(rdd_more_numbers).collect()

  // Cartesian product
  rdd_numbers.cartesian(rdd_more_numbers).collect()
  rdd_numbers.cartesian(rdd_more_numbers).map(x => x._1 + x._2).collect()

  // SortByKey
  rdd_more_numbers.cartesian(rdd_numbers).collect()
  rdd_more_numbers.cartesian(rdd_numbers).sortByKey().collect()
  rdd_more_numbers.cartesian(rdd_numbers).sortByKey(false).collect()

  // CountByValue
  val rdd_many_numbers = rdd_numbers.union(rdd_more_numbers)
  rdd_many_numbers.collect()
  rdd_many_numbers.countByValue()

  // EJERCICIO 2:
  // Calcular el número de ocurrencia de cada palabra en rdd_lines
  rdd_lines.flatMap(_.split(" ")).countByValue().take(10)

  // Top
  rdd_more_numbers.collect()
  rdd_more_numbers.top(3)
  rdd_more_numbers.distinct().top(3)

  // TakeOrdered
  rdd_more_numbers.collect()
  rdd_more_numbers.takeOrdered(3)
  rdd_more_numbers.takeOrdered(3)(Ordering.Int.reverse)

  // Reduce
  rdd_more_numbers.collect()
  rdd_more_numbers.reduce(_ + _)
  rdd_more_numbers.reduce(_ * _)

  // Fold
  rdd_more_numbers.collect()
  rdd_more_numbers.fold(0) { case (acc, element) => acc + element }
  rdd_more_numbers.fold(1) { case (acc, element) => acc * element }

  // Aggregate
  // Función de agregación por partición
  val seqOp = (acc: Int, elem: Int) => acc + elem
  // Función de combinación
  val combOp = (acc1: Int, acc2: Int) => acc1 + acc2
  // Aplicar función aggregate
  rdd_more_numbers.aggregate(0)(seqOp, combOp)

  // ReduceByKey
  rdd_numbers.cartesian(rdd_more_numbers).collect()
  val reducedRDD = rdd_numbers.cartesian(rdd_more_numbers).reduceByKey(_ + _)
  spark.time(reducedRDD.collect())

  // Scala: String interpolation
  reducedRDD.map(tuple => s"Grupo ${tuple._1} --> Valor: ${tuple._2}").collect()

  // RDD Partitioning
  reducedRDD.toDebugString

  rdd_numbers.getNumPartitions
  rdd_more_numbers.getNumPartitions

  val reducedRDD2 = rdd_numbers.repartition(2).cartesian(rdd_more_numbers.repartition(2)).reduceByKey(_ + _)
  reducedRDD2.toDebugString

  val reducedRDD3 = rdd_numbers.coalesce(2).cartesian(rdd_more_numbers.coalesce(2)).reduceByKey(_ + _)
  reducedRDD3.toDebugString

  // EJERCICIO 3:
  // Contador de las palabras Spark y Scala de rdd_lines utilizando reduceByKey
  rdd_lines.flatMap(_.split(" ")).filter(w => w.equals("Scala") || w.equals("Spark")).map(w => (w, 1)).reduceByKey(_ + _).collect()

  // EJERCICIO 4:
  // Usando %3, sumar los números divisibles por %3==0, %3==1 o %3==2 (como si fuera por grupo)
  // Aplicarlo sobre una colección de 0 a 99
  sc.parallelize(Range(0, 100)).map(x => (x % 3, x)).reduceByKey(_ + _).collect()

  spark.close()
}
