package com.juan.procesamientodatos
package sparkClase.sql

import sparkClase.SparkProvider

import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

object exercise_sparkSQL extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  import spark.implicits._

  val winesFilename = "src/main/scala/files/winequality-red-white.txt"
  val winesdf = spark.read
    .format("csv")
    .option("header", "true")
    .option("delimiter", "|")
    .option("inferSchema", "true")
    .load(winesFilename)

  // 1. Obtener una muestra de ejemplo del DF por pantalla
  winesdf.show()

  // 2. Visualizar el esquema o estructura del DF
  winesdf.printSchema()

  // 3. Quedarnos solo con los nombres de las columnas que albergan datos de tipo "double"
  val double_cols = winesdf.dtypes.filter { case (_, t) => t == "double" }.map(_._1)

  // 4. Descripción estadística de las variables “fixed_acidity” y "citric_acid" simultáneamente
  winesdf.describe("fixed_acidity", "citric_acid").show()

  // 5. Número de muestras total en el dataset
  winesdf.count()

  // 6. Número de filas distintas en el dataset
  winesdf.distinct().count()

  // 7. Hay vinos iguales?
  winesdf.count() > winesdf.distinct().count()

  // 8. Número de nulos en cada columna
  val all_cols = winesdf.columns
  val null_counts: Seq[org.apache.spark.sql.Column] = all_cols.map(c => sum(col(c).isNull.cast("int")).alias(c + "_nulls"))
  winesdf.select(null_counts: _*).show()
  winesdf.agg(null_counts.head, null_counts.tail: _*).show()

  // 9. Cuántos vinos hay de cada tipo
  winesdf.groupBy("style").agg(count("*").alias("num_wines")).show()

  // 10. Comparar tintos vs blancos en términos de acidez y calidad
  winesdf.groupBy("style")
    .agg(
      count("*").alias("count"),
      mean("fixed_acidity").alias("mean_fixed_acidity"),
      stddev("fixed_acidity").alias("std_fixed_acidity"),
      mean("quality").alias("mean_quality"),
      stddev("quality").alias("std_quality")
    )
    .show()

  // 11. Nueva columna porcentaje de SO2 libre
  winesdf.withColumn(
    "pcg_free_sulfur_dioxide",
    col("free_sulfur_dioxide") / col("total_sulfur_dioxide")
  ).show()

  // 12. Nueva columna chloride_per_citric_acid
  winesdf.withColumn(
    "chloride_per_citric_acid",
    when(col("citric_acid") === 0, lit(-1.0))
      .otherwise(col("chlorides") / col("citric_acid"))
  ).show()

  // 13. Nueva columna id del vino
  val winesiddf = winesdf.withColumn("id", monotonically_increasing_id())

  // 14. Valor medio de fixed_acidity
  winesdf.select(mean("fixed_acidity")).show()

  // 15. Recoger el valor medio en una variable
  val mean_fixed_acidity =
    winesdf.select(mean("fixed_acidity").alias("mean_fixed_acidity"))
      .first()
      .getAs[Double]("mean_fixed_acidity")

  // 16. Cuántos vinos hay con fixed_acidity superior a la media
  winesdf.filter(col("fixed_acidity") > mean_fixed_acidity).count()

  // 17. Media de fixed_acidity en blancos y tintos en un Map[String, Double]
  val mean_fixed_acidity_map =
    winesdf.groupBy("style")
      .agg(mean("fixed_acidity").alias("mean_fixed_acidity"))
      .rdd
      .map(r => (r.getAs[String]("style"), r.getAs[Double]("mean_fixed_acidity")))
      .collectAsMap()

  // 18. Incremento relativo de fixed_acidity respecto a la media de su categoría
  val wStyle = Window.partitionBy("style")

  val winesWithIncDf = winesdf
    .withColumn("cat_avg_fixed_acidity", mean("fixed_acidity").over(wStyle))
    .withColumn(
      "inc_fixed_acidity",
      (col("fixed_acidity") - col("cat_avg_fixed_acidity")) / col("cat_avg_fixed_acidity")
    )

  // 19. En cada categoría, cuántos vinos tienen fixed_acidity superior a la media de su categoría
  winesWithIncDf
    .filter(col("fixed_acidity") > col("cat_avg_fixed_acidity"))
    .groupBy("style")
    .agg(count("*").alias("num_above_cat_mean"))
    .show()

  // 20. alcohol_label
  val alclabelf = winesdf.withColumn(
    "alcohol_label",
    when(col("alcohol") < 9.5, "low")
      .when(col("alcohol") >= 12.0, "high")
      .otherwise("medium")
  )

  alclabelf.show()

  // 21. Promedio de cada variable numérica por etiqueta de alcohol
  val mean_double_cols: Seq[org.apache.spark.sql.Column] = double_cols.map(c => mean(c).alias("mean_" + c))
  alclabelf.groupBy("alcohol_label").agg(mean_double_cols.head, mean_double_cols.tail: _*).show()

  // 22. Promedio y std de cada variable numérica por etiqueta de alcohol, redondeado a 4 decimales
  val mean_std_double_cols: Seq[org.apache.spark.sql.Column] = double_cols.flatMap(c =>
    List(
      round(mean(c), 4).alias("mean_" + c),
      round(stddev(c), 4).alias("std_" + c)
    )
  )

  alclabelf.groupBy("alcohol_label").agg(mean_std_double_cols.head, mean_std_double_cols.tail: _*).show()

  // 23. Mostrar en orden descendente combinaciones de categoría y nivel de alcohol según pH medio
  alclabelf
    .groupBy("style", "alcohol_label")
    .agg(mean("pH").alias("mean_pH"))
    .orderBy(desc("mean_pH"))
    .show()

  // 24. Primer y tercer cuartil de total_sulfur_dioxide
  winesdf.stat.approxQuantile("total_sulfur_dioxide", Array(0.25, 0.75), 0.0)

  // 25. Nos quedamos solo con vinos no repetidos
  val cols = winesdf.columns
  val wAll = Window.partitionBy(cols.map(col): _*)

  val winesNoRepDf = winesdf
    .withColumn("num_reps", count("*").over(wAll))
    .filter(col("num_reps") === 1)
    .drop("num_reps")

  // 26. En qué categoría hay más vinos que no se repiten
  val winesRepFlagDf = winesdf
    .withColumn("num_reps", count("*").over(wAll))
    .withColumn("norep", when(col("num_reps") === 1, 1).otherwise(0))

  winesRepFlagDf
    .groupBy("style")
    .agg(sum("norep").alias("num_norep"))
    .orderBy(desc("num_norep"))
    .show()

  // 27. Etiqueta con cuartil de pH por tipo de vino
  val wPH = Window.partitionBy("style").orderBy("pH")

  val phlabeldf = winesdf.withColumn("pH_quartile", ntile(4).over(wPH))

  phlabeldf.show()

  // 28. Test: mínimo y máximo de pH por tipo de vino y cuartil
  phlabeldf
    .groupBy("style", "pH_quartile")
    .agg(
      min("pH").alias("min_pH"),
      max("pH").alias("max_pH")
    )
    .orderBy("style", "pH_quartile")
    .show()

  // 29. Matriz de correlaciones
  val pairs = double_cols.toSet.subsets(2).toArray.map(_.toArray).map {
    case Array(f1, f2) => (f1, f2)
  }

  val corr_matrix_df = pairs.map { p =>
    val rho = winesdf.stat.corr(p._1, p._2)
    (p._1, p._2, rho)
  }.toSeq.toDF("feature1", "feature2", "correlation")

  // 30. Ordenar pares por correlación descendente
  corr_matrix_df.orderBy(desc("correlation")).show(false)

  // 31. Ordenar por magnitud de la correlación
  corr_matrix_df
    .withColumn("abs_correlation", abs(col("correlation")))
    .orderBy(desc("abs_correlation"))
    .show(false)

  // 32. Dataset artificial de tiendas de vino
  val wine_id = winesiddf.select("id").distinct().rdd
    .map(r => r.getAs[Long]("id").toInt)
    .collect()
    .zipWithIndex
    .map { case (a, b) => (b, a) }
    .toMap

  val num_wines = wine_id.size.toDouble

  val r = scala.util.Random

  val get_wine_id = udf((code: Int) => {
    if ((code % 3) == 0) 20000 + r.nextInt(1000) else wine_id(code)
  })

  val shopdf = spark.sqlContext.range(500)
    .withColumn("shop_id", round(lit(20000.0) * rand()).cast("int"))
    .withColumn("city_code", round(lit(7.0) * rand()).cast("int"))
    .withColumn("city", lit("none"))
    .withColumn("city", when(col("city_code") === 0, "Madrid").otherwise(col("city")))
    .withColumn("city", when(col("city_code") === 1, "Sevilla").otherwise(col("city")))
    .withColumn("city", when(col("city_code") === 2, "Barcelona").otherwise(col("city")))
    .withColumn("city", when(col("city_code") === 3, "Zaragoza").otherwise(col("city")))
    .withColumn("city", when(col("city_code") === 4, "Valencia").otherwise(col("city")))
    .withColumn("city", when(col("city_code") === 5, "Valladolid").otherwise(col("city")))
    .withColumn("city", when(col("city_code") === 6, "Malaga").otherwise(col("city")))
    .withColumn("city", when(col("city_code") === 7, "Bilbao").otherwise(col("city")))
    .withColumn("id_code", round(lit(num_wines - 1.0) * rand()).cast("int"))
    .withColumn("id_wine", get_wine_id(col("id_code")))
    .withColumn("balance", lit(5.0) * randn() + lit(90.0))
    .drop("id", "city_code", "id_code")

  // 33. Número de tiendas por ciudad
  shopdf.groupBy("city").agg(count("*").alias("num_shops")).show()

  // 34. Número de tiendas diferentes por ciudad
  shopdf.groupBy("city").agg(countDistinct("shop_id").alias("num_distinct_shops")).show()

  // 35. Cuántos de los vinos iniciales pueden encontrarse en las tiendas
  shopdf.select("id_wine").distinct()
    .join(winesiddf.select(col("id").alias("id_wine")), Seq("id_wine"))
    .count()

  spark.stop()
}
