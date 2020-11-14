package spark

import org.apache.spark.sql.{DataFrame, Row}
import org.apache.spark.sql.functions.{col, lower}

class DataFrameTransformation {
  private val df: DataFrame = ReadParquet.getDataFrame()

  //add new column
  val patternDF = df
    .withColumn("pattern", lower(col("pattern")))
    .withColumn("dt", col("key"))

  //make array from date frame
  private val array: Array[Row] = patternDF.collect()
  private val strings: Array[String] = array.map(x => {
    "test"
  })


  def join() = {
    val s = ReadParquet.getDataFrame().as("s")
    val c = ReadParquet.getDataFrame().as("c")
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
    val s = ReadParquet.getDataFrame()
    s.selectExpr("colA", "colB as newName", "abs(colC)")
  }

  def dedup() = {
    val s = ReadParquet.getDataFrame()
    s.dropDuplicates(Seq("aid", "mrt", "msg"))
  }
}
