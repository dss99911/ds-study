package spark

import org.apache.spark.broadcast

/**
 * copy data to each cluster.
 * and read-only.
 */
class Broadcast {
  val spark = SparkSessionCreate.createSparkSession()
  private val data: broadcast.Broadcast[String] = spark.sparkContext.broadcast("1")

  data.value
}
