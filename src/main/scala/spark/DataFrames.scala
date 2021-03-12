package spark

import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{LongType, TimestampType}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import spark.Read.Person

class DataFrames {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()

  //add new column
  val patternDF = df
    .select("name")

    .select('age) //col() with shortest way
    .selectExpr("*") //include all original columns
    .select(col("count").alias("fail_count")) //alias
    .select(lit(1).as("num")) //able to set liternal with name
    .withColumn("dt", $"key")
    .withColumn("dt", lit("dd"))
    .drop($"age") //drop column

  //order by
  patternDF
    //age asc
    .orderBy("age")
    .sort("age")
    //age desc
    .orderBy(desc("age"))
    .orderBy(expr("age desc"))
    .orderBy(asc_nulls_first("age"))
    .orderBy($"age".desc)
    .sort($"age".desc)

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
    //만약 partition이 어느정도 나눠져 있다면(aid-prefix로 나눠져 있는 등), 셔플 없이, dedup이 빠르게 처리됨.
    s.dropDuplicates(Seq("aid", "mrt", "msg"))
  }

  def useOnSql() = {
    df.createOrReplaceTempView("people")
    spark.sql("SELECT * FROM people")

    // Register the DataFrame as a global temporary view
    // temp view is disappeared when session expired
    // global temp view is disappeared when spark app is terminated
    // data is not processed when temp view is created.
    df.createGlobalTempView("people")
    spark.sql("SELECT * FROM global_temp.people").show()
  }

  def convertDataFrameToObject() = {
    Read.getCsv()
      .as[Person] //convert to object
      .map(p => p.age)
      .show()
  }


  def makeList() = {
    //this approach use driver program,
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

  def unionDF() = {
    val df2 = df
    //union should have same columns.
    //also columns order should be same
    df.union(df2.select(df.columns.map(col(_)): _*))

    //no need same order. just name should be same
    df.unionByName(df2)
    //no need same order. if other dataframe contains columns which not exist on other dataframe. the columns' value is null
    df.unionByName(df2, true)
  }

  def underscoreToCamelDataFrame(df: DataFrame): DataFrame = {
    def underscoreToCamel(s: String): String = {
      val split = s.split("_")
      val tail = split.tail.map { x => x.head.toUpper + x.tail }
      split.head + tail.mkString
    }

    df.columns.foldLeft(df)((df: DataFrame, colName: String) => df.withColumnRenamed(colName, underscoreToCamel(colName)))
  }

  def camelToUnderscoresDataFrame(df: DataFrame): DataFrame = {
    def camelToUnderscores(name: String) = "[A-Z\\d]".r.replaceAllIn(name, { m =>
      "_" + m.group(0).toLowerCase()
    })

    df.columns.foldLeft(df)((df: DataFrame, colName: String) => df.withColumnRenamed(colName, camelToUnderscores(colName)))
  }

  def findFunctions() = {
    //check functions on the package of the below
    org.apache.spark.sql.functions
  }
}
