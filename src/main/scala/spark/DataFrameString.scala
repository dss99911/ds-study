package spark

import org.apache.spark.sql.functions.{concat, concat_ws, expr, instr, length, lit, lower, regexp_extract, regexp_replace, substring}
import org.apache.spark.sql.{DataFrame, SparkSession}

class DataFrameString {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

    df
      .withColumn("pattern", lower($"pattern"))
      .withColumn("pattern", substring($"pattern", 0, 4)) //first 4 digit
      .withColumn("pattern", $"pattern".substr(length($"pattern") - 3, lit(4))) //last 4 digit. start from index 1
      .withColumn("pattern", $"pattern".substr(-4, 4)) //last 4 digit. start from index 1
      .withColumn("number", regexp_extract($"number", "(\\w+)", 1)) //take only word
      .withColumn("number", regexp_replace($"sms_body", "\n", " "))
      .withColumn("number", expr("col_name rlike '^.*$'"))
      .withColumn("concats", concat($"number", $"name")) // concat string
      .withColumn("concats", concat_ws("_", $"number", $"name")) // concat string with delimeter
      .filter($"text".rlike("regex"))
      .withColumn("instr", instr($"name", "TEST") >= 1) //substring에 해당하는 텍스트의 첫 인덱스(인덱스는 1 부터 시작함)Returns the (1-based) index of the first occurrence of substr in str.
}
