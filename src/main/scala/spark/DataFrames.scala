package spark

import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.apache.spark.sql.functions.{col, desc, lit, lower, typedLit}

class DataFrames {
  private val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._
  private val df: DataFrame = Read.getParquetDataFrame()

  //add new column
  val patternDF = df
    .select("name")
    .select($"age" + 1) //able to use expr
    .select(col("count").alias("fail_count")) //alias
    .withColumn("pattern", lower($"pattern"))
    .withColumn("dt", $"key")
    .withColumn("dt", lit("dd"))
    .withColumn("dt", typedLit(Seq(1, 2, 3)))
    .filter(col("age") > 20)
    .drop($"age")//drop column
    .groupBy("age").count()// (age, count), count()'s column name is 'count'

  //order by
  patternDF
    //age asc
    .orderBy("age")
    .sort("age")
    //age desc
    .orderBy(desc("age"))
    .orderBy($"age".desc)
    .sort($"age".desc)


  //make array from date frame
  private val array: Array[Row] = patternDF.collect()
  private val strings: Array[String] = array.map(x => {
    "test"
  })

  //show schema
  df.printSchema()

  //show data
  df.show()


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

  def makeRaw() = {
    //https://stackoverflow.com/questions/32000646/extract-column-values-of-dataframe-as-list-in-apache-spark
    // there are 2 recommended approach. not sure what is better
    val list = df.select("id").map(r => r.getString(0)).collect

    val list1 = df.select("id").rdd.map(r => r(0)).collect
  }

}
