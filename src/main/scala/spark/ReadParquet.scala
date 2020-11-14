package spark

import org.apache.spark.sql.{DataFrame, SparkSession}

object ReadParquet {
  def getDataFrame(): DataFrame = {
    val spark: SparkSession = SparkSessionCreate.createSparkSession()
    spark.read.parquet("s3://text")
  }

}
