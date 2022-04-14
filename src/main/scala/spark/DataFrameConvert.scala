package spark

import org.apache.spark.sql.functions.{expr, lit, sha2, when}
import org.apache.spark.sql.{DataFrame, SparkSession}

class DataFrameConvert {

  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

  df
    .select($"age" + 1) //able to use expr
    .select(expr("age + 1"))
    .na.fill("this is null") //change null to some value
    .na.fill(Map("age" -> 0, "name" -> "unknown")) //change null to some value
    .na.replace("age", Map(10 -> 20, 11 -> 21)) //이건 null과 관련 없이 값 변환

  def whenOther() = {

    df
      .withColumn("date", when($"age" === lit(1), "it's 1")
        .when($"age" === lit(1), "it's 1")
        .otherwise("no 1")
      )
  }

  def whenValueNull() = {
    df.map { r =>
      val a = Option(r.getAs[String]("some"))
      a
    }
  }
  def hash() = {
    df.withColumn("hash", sha2($"a" + $"b" + $"c" + $"date".cast("string"), 256))

  }

}
