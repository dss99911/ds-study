package spark

import org.apache.spark.sql.functions.{explode, typedLit}
import org.apache.spark.sql.{DataFrame, SparkSession}

class DataFrameObject {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

  df
    // object를 바깥으로 빼기
    // https://stackoverflow.com/questions/32906613/flattening-rows-in-spark
    .withColumn("exp", explode($"array")) //해당 값들을 row들로 변환한다.
    .withColumn("exp", explode($"obj.data"))
    .withColumn("dt", typedLit(Seq(1, 2, 3)))
}
