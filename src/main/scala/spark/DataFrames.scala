package spark

import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.apache.spark.sql.functions.{col, lower}

class DataFrames {
  private val spark: SparkSession = SparkSessionCreate.createSparkSession()
  import spark.implicits._
  private val df: DataFrame = Read.getParquetDataFrame()

  //add new column
  val patternDF = df
    .select("name")
    .select(col("age") + 1) //able to use expr
    .withColumn("pattern", lower($"pattern"))
    .withColumn("dt", $"key")
    .filter(col("age") > 20)
    .groupBy("age").count()// (age, count)

  //make array from date frame
  private val array: Array[Row] = patternDF.collect()
  private val strings: Array[String] = array.map(x => {
    "test"
  })

  //show schema
  df.printSchema()

  //show data
  df.show()


  def join() = {
    val s = Read.getParquetDataFrame().as("s")
    val c = Read.getParquetDataFrame().as("c")
    s.join(c, col("s.id") === col("c.id"))
      .select(
        col("s.id").alias("id"),
        col("c.code").alias("code"),
        col("s.text").alias("text")
      ).where("c.status = 1")
  }

  /**
   * expression
   */
  def selectExpr() = {
    val s = Read.getParquetDataFrame()
    s.selectExpr("colA", "colB as newName", "abs(colC)")
  }

  def dedup() = {
    val s = Read.getParquetDataFrame()
    s.dropDuplicates(Seq("aid", "mrt", "msg"))
  }

  def useOnSql() = {
    df.createOrReplaceTempView("people")
    spark.sql("SELECT * FROM people")
  }


}
