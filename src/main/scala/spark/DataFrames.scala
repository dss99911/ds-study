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
    .select($"count" as "other_count")
    .select(lit(1).as("num")) //able to set liternal with name
    .withColumn("dt", $"key")
    .withColumn("dt", lit("dd"))
    .drop($"age") //drop column

  //Sort, order
  //주의사항
  // - 정렬 후에 repartition하면, 정렬이 파티션별로 섞이게됨.
  // - repartition후에 정렬을 하면, partition갯수가 바뀔 수 있음
  // - 파일을 하나만 만들면서, 정렬도 하고 싶다면, coalesce(1)를 하기
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
    // 중복중 마지막을 남기고, 앞에 거를 없앰. 하지만, 순서가 중요하다면, windows로 필터링하는게 명시적으로 좋을듯.
    s.dropDuplicates(Seq("aid", "mrt", "msg"))
  }

  def useOnSql() = {
    //tempView를 만든다고, 메모리에 유지되는 건 아니고, table로 연결시켜주는 역할만 하는 것으로 보임
    //가령, scala로 작성한 코드의 데이터를 python에서 참조하고 싶을 때.
    df.createOrReplaceTempView("people")
    spark.sql("SELECT * FROM people")

    // Register the DataFrame as a global temporary view
    // temp view is disappeared when session expired
    // global temp view is disappeared when spark app is terminated
    // data is not processed when temp view is created.
    df.createGlobalTempView("people")
    spark.sql("SELECT * FROM global_temp.people").show()
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
    val frame = Read.getCsv()
    frame.map(teenager => teenager.getValuesMap[Any](frame.columns)).collect()
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

    val dfs = Seq(df, df, df)
    dfs.reduce(_ union _)
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
