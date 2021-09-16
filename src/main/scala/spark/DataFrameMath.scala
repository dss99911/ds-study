package spark

import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, SparkSession}

class DataFrameMath {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

    df
      .withColumn("aa", expr("conv(decimal_value, 10, 16)"))
      .withColumn("aa", expr("conv(hex_value, 16, 10)"))
}
