package spark

import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.apache.spark.sql.functions.{col, desc, lit, lower, typedLit}
import org.apache.spark.sql.types.TimestampType
import spark.Read.Person

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
    .withColumn("date", ($"date" / 1000).cast(TimestampType)) // long to Timestamp
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

    // Register the DataFrame as a global temporary view
    // temp view is disappeared when session expired
    // global temp view is disappeared when spark app is terminated
    df.createGlobalTempView("people")
    spark.sql("SELECT * FROM global_temp.people").show()
  }

  def convertDataFrameToObject() = {
    Read.getCsv().as[Person]//convert to object
      .map(p => p.age)
      .show()
  }

  def makeList() = {
    //https://stackoverflow.com/questions/32000646/extract-column-values-of-dataframe-as-list-in-apache-spark
    // there are 2 recommended approach. not sure what is better
    val list = df.select("id").map(r => r.getString(0)).collect

    val list1 = df.select("id").rdd.map(r => r(0)).collect
  }

  def convertDataFrameToMap() = {
    // No pre-defined encoders for Dataset[Map[K,V]], define explicitly
    implicit val mapEncoder = org.apache.spark.sql.Encoders.kryo[Map[String, Any]]
    // Primitive types and case classes can be also defined as
    // implicit val stringIntMapEncoder: Encoder[Map[String, Any]] = ExpressionEncoder()

    // row.getValuesMap[T] retrieves multiple columns at once into a Map[String, T]
    Read.getCsv().map(teenager => teenager.getValuesMap[Any](List("name", "age"))).collect()
    // Array(Map("name" -> "Justin", "age" -> 19))
  }

}
