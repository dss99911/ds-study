package spark

import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}

object Read {
  val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._

  def getParquetDataFrame(): DataFrame = {
    spark.read.parquet("s3://text")
  }

  def getGlobPatternParquetDatFrame(): DataFrame = {
    //https://hadoop.apache.org/docs/r2.7.2/api/org/apache/hadoop/fs/FileSystem.html#globStatus(org.apache.hadoop.fs.Path)
    spark.read.parquet("s3://text/*/aa")

    //load only .parquet file. https://spark.apache.org/docs/latest/sql-data-sources-generic-options.html#path-global-filter
    spark.read.format("parquet")
      .schema(StructTypes.sample())//set schema. for prod environment. setting schema is recommended
      .option("pathGlobFilter", "*.parquet") // json file should be filtered out
      .load("examples/src/main/resources/dir1")

    //load files recursively. https://spark.apache.org/docs/latest/sql-data-sources-generic-options.html#recursive-file-lookup
    spark.read.format("parquet")
      .option("recursiveFileLookup", "true")
      .load("examples/src/main/resources/dir1")
  }

  def getFromMultiplePath(): DataFrame = {
    spark.read.parquet("s3://a", "s3://a1", "s3://a2")
  }

  def getJdbcDataFrame(): DataFrame = {
    val DB_URL, DATABASE, TABLE, USERNAME, PASSWORD = ""

    spark.read.format("jdbc")
      .option("url", DB_URL)
      .option("dbtable", s"$DATABASE.$TABLE")
      .option("user", USERNAME)
      .option("password", PASSWORD)
      .option("driver", "com.mysql.cj.jdbc.Driver")
      .load()
  }

  /**
   * get the text. a row is a line
   * @return
   */
  def getTextDataSet(): (SparkSession, Dataset[String]) = {
    (spark, spark.read.textFile("README.md"))
  }

  def getSqlDataFrame(): DataFrame = {
    spark.sql("select * from some")
  }

  /**
   * toDF() is not recommended on prod.
   * because toDF may not work properly related to null value
   */
  def getListDataFrame() = {
    val list = (1 to 100).map(i => (i, s"val_$i"))
    list.toDF()

    //or
    val rows = Seq(Row(1), Row(2), Row(3))
    val rdd = spark.sparkContext.parallelize(rows)
    spark.createDataFrame(rdd, StructTypes.sample())
  }

  def getListDataSet() = {
    val list = (1 to 100).map(i => (i, s"val_$i"))
    list.toDS()
  }

  case class Person(name: String, age: Long)

  def getClassDataSet() = {
    // Encoders are created for case classes
    Seq(Person("Andy", 32)).toDS()
  }

  def getJsonToClassDataSet() = {
    spark.read.json("path").as[Person]
  }

  def getTable() = {
    //if database is specified
    spark.table("mms.company")
  }

  def getCsv() = {
    //format ex) 1,abcd,"asdfsd""dd""f" ==> quote in string
    //format ex) 1,abcd,"as
    // dfsd""dd""f"  ==> two line
    spark.read
      .option("header","true")//set first row as header
      .option("multiline",true)//if data contain new line
      .option("quote", "\"")//if using multiline, this is required if text contains "
      .option("escape", "\"")//if using multiline, this is required if text contains "
      .csv("s3://hyun/aaa.csv")
  }

  /**
   * https://spark.apache.org/docs/latest/sql-data-sources-generic-options.html#ignore-corrupt-files
   */
  def ignoreCorruptFile() = {
    /*
dir1/
 ├── dir2/
 │    └── file2.parquet (schema: <file: string>, content: "file2.parquet")
 └── file1.parquet (schema: <file, string>, content: "file1.parquet")
 └── file3.json (schema: <file, string>, content: "{'file':'corrupt.json'}")
     */

    // enable ignore corrupt files
    spark.sql("set spark.sql.files.ignoreCorruptFiles=true")
    // dir1/file3.json is corrupt from parquet's view
    val testCorruptDF = spark.read.parquet(
      "examples/src/main/resources/dir1/",
      "examples/src/main/resources/dir1/dir2/")
    testCorruptDF.show()
    // +-------------+
    // |         file|
    // +-------------+
    // |file1.parquet|
    // |file2.parquet|
    // +-------------+
  }

  /**
   * merge partition when reading
   */
  def readPartitionsHasDifferentColumn() = {
    //https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#schema-merging
  }

}
