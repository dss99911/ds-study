package spark

import org.apache.spark.sql.SparkSession

object SparkSessionCreate {
  def createSparkSession(): SparkSession = {
    val spark = SparkSession.builder.appName("acs_tx_extractor").enableHiveSupport().getOrCreate()
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    spark
  }
}
