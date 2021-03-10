package spark

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.{current_timestamp, date_format, from_utc_timestamp, lit, when}
import org.apache.spark.sql.types.{LongType, TimestampType}

class DataFrameTimestamp {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

  df
    .withColumn("date", ($"date" / 1000).cast(TimestampType)) // ms long to Timestamp
    .withColumn("date", when($"age" === lit(1), "it's 1").otherwise("no 1"))
    .withColumn("transactionAt", ($"transactionAt" / 1000).cast(TimestampType)) //change long to timestamp
    .withColumn("transactionAt", $"transactionAt".cast(LongType)) //change timestamp to long
    .withColumn("transactionAt", from_utc_timestamp(($"transactionAt" / 1000).cast(TimestampType), "+05:30")) //change long to timestame with india zone
    .withColumn("transactionAt", date_format(current_timestamp(),"yyyy MM dd"))

}
