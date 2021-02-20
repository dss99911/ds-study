package spark

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.{row_number, window}
import org.apache.spark.sql.types.TimestampType

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

  def groupByDate() = {
    val a = Seq(System.currentTimeMillis() / 1000,2,3,4,5)

    a.toDF().withColumn("date", $"value".cast(TimestampType))
      .groupBy(window($"date", "1 day"))
      .count()

      .show(truncate = false)

    //    [1970-01-01 00:00:00, 1970-01-02 00:00:00]	4
    //    [2021-02-17 00:00:00, 2021-02-18 00:00:00]	1
  }
}
