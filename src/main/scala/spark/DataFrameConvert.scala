package spark

import org.apache.spark.sql.functions.{expr, lit, sha2, when, col}
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

  def null_vaue(df: DataFrame) = {
    // null을 가공해도 null이 됨
    //
    // |: 둘중 하나라도 true이면, true. 하나가 false이면, 다음 값을 따라감. 순서 상관 없음
    //   - null | true => true
    //   - null | false => null
    // &: 하나라도 false이면 false. 하나가 true이면, 다음 값을 따라감. 순서 상관 없음.
    //   - null & false => false
    //   - null & true => null
      df.withColumn("null_1", col("null_value") + 1)
      .withColumn("null_2", col("null_value") > 0)
      .withColumn("true_1", (col("null_value") > 0) || lit(true))
      .withColumn("null_3", (col("null_value") > 0) || lit(false))
      .withColumn("false_1", (col("null_value") > 0) && lit(false))
      .withColumn("null_4", (col("null_value") > 0) && lit(true))
      .withColumn("true_2", lit(true) || (col("null_value") > 0))
      .withColumn("null_4", lit(false) || (col("null_value") > 0))
      .withColumn("false_2", lit(false) && (col("null_value") > 0))
      .withColumn("null_5", lit(true) && (col("null_value") > 0))
  }

}
