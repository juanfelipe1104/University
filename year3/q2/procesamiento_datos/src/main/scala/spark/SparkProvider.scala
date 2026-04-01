package com.juan.procesamientodatos
package spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkContext

object SparkProvider {
  lazy val spark: SparkSession = SparkSession.builder()
    .appName("ProcesamientoDatos")
    .master("local[*]")
    .getOrCreate()

  lazy val sc: SparkContext = spark.sparkContext
}
