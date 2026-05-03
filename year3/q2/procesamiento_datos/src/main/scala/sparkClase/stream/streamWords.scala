package com.juan.procesamientodatos
package sparkClase.stream

import sparkClase.SparkProvider

import org.apache.spark.sql._
import org.apache.spark.sql.functions.{current_timestamp, window}
import org.apache.spark.sql.streaming._

object streamWords extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  val lines = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()
  val words = lines.as[String].flatMap(_.split(" "))
  val wordCounts = words.groupBy("value").count()

  def preprocessBatch(batchDF: DataFrame, batchId: Long): Unit = {
    batchDF.coalesce(1).write.mode("overwrite").csv("/opt/spark/work-dir/streaming1csv/")
    batchDF.coalesce(1).write.mode("overwrite").json("/opt/spark/work-dir/streaming1json/")
  }

  val stream1 = wordCounts.writeStream.foreachBatch(preprocessBatch).start()
}

object streamWords2 extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  val lines = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()
  val words = lines.as[String].flatMap(_.split(" "))
  val wordCounts = words.withColumn("timestamp", current_timestamp()).groupBy(window($"timestamp", "30 seconds")).count()
  wordCounts.writeStream.outputMode("complete").format("console").trigger(Trigger.ProcessingTime("30 seconds")).start()
}

object streamWords3 extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  val lines = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()
  val words = lines.as[String].flatMap(_.split(" "))
  val wordCounts = words.groupBy("value").count()
  wordCounts.writeStream.outputMode("complete").format("console").trigger(Trigger.Once()).start()
}

object streamWords4 extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  val lines = spark.readStream.format("text").load("/root/")
  val words = lines.as[String].flatMap(_.split(" "))
  val wordCounts = words.groupBy("value").count()
  val stream = wordCounts.writeStream.outputMode("complete").format("console").start()
}

object streamWords5 extends App {
  val spark = SparkProvider.spark
  val sc = SparkProvider.sc
  val lines = spark.readStream.format("text").load("/root/")
  val words = lines.as[String].flatMap(_.split(" "))
  val wordCounts = words.groupBy("value").count()
  val stream = wordCounts.writeStream.outputMode("complete").format("kafka")
}