package spark

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.{current_date, current_timestamp, date_add, date_format, date_sub, datediff, from_utc_timestamp, lit, months_between, to_date, to_timestamp, when}
import org.apache.spark.sql.types.{LongType, TimestampType}

class DataFrameTimestamp {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

  df
    //long to timestamp
    .withColumn("date", ($"date" / 1000).cast(TimestampType)) // ms long to Timestamp
    //long to timestamp(change timezone)
    .withColumn("transactionAt", from_utc_timestamp(($"transactionAt" / 1000).cast(TimestampType), "+05:30")) //change long to timestame with india zone
    //timestamp to long
    .withColumn("transactionAt", $"transactionAt".cast(LongType)) //change timestamp to long
    //formatting to string
    .withColumn("transactionAt", date_format(current_timestamp(),"yyyy MM dd"))
    //string to timestamp
    .withColumn("transactionAt", to_date(lit("2016-01-01")))
    .withColumn("transactionAt", to_date(lit("2016-01-01"), "yyyy-MM-dd"))
    .withColumn("transactionAt", to_timestamp(lit("2016-01-01 11:22:23"), "yyyy-MM-dd HH:mm:ss"))
    .withColumn("transactionAt", to_timestamp(lit("2016-01-01 11:22:23")))//yyyy-MM-dd HH:mm:ss 를 기본값으로 사용.
    //today, now
    .withColumn("today", current_date())
    .withColumn("now", current_timestamp())
    //plus, minus the date
    .select(date_sub('now, 5), date_add('now, 5))
    //diff
    .select(datediff('date1, 'date2))
    .select(months_between('date1, 'date2))
    //compare
    .filter('date > lit("2020-11-23"))
    .filter('date > "2020-11-23")
}
