package spark

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.row_number

class WindowFunctions {
  val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()
    df.withColumn("rank",
      row_number().over(
        Window
          .partitionBy("pattern_id", "error_message")
          .orderBy("pattern_id", "error_message")))

  def getFirstRowOfGroup() = {
    import org.apache.spark.sql.SaveMode
    import org.apache.spark.sql.expressions.Window

    val w = Window.partitionBy("type").orderBy("type")
    df.withColumn("rn", row_number.over(w))
      .where($"rn" === 1).drop("rn")
      .write
      .mode(SaveMode.Overwrite)
      .parquet("s3://hyun/temp/test")


  }
}
