package spark

import org.apache.spark.sql.functions.col
import org.apache.spark.sql.{DataFrame, SparkSession}

class DataFrameFilter {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

  df
    .filter(col("age") > 20)
    .filter('age =!= 1) //!=
    .na.drop(Seq("name")) //drop null rows if name column is null
    .na.drop("any") //drop row if any columns are null
    .na.drop("all", Seq("age", "name")) //drop row if all columns are null

  //like any, like all
  //https://issues.apache.org/jira/browse/SPARK-30724
}
