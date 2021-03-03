package spark

import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions.{explode, typedLit, udf}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}

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


  //object를 컬럼에 넣기
  val objectUDF: UserDefinedFunction = udf((num: Int) => {
    T("a", "B", num)
  })
  import spark.implicits._
  Seq(1, 2, 3)
    .toDF("value")
    .withColumn("test", objectUDF($"value"))
  //nested column을 밖으로 빼기
    .selectExpr("test.*", "*")
  //안쓰는 컬럼 삭제
    .drop("value", "test")
    .show()


}

case class T(a: String, b: String, num: Int)
