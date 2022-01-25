package spark

import org.apache.spark.sql.types.{IntegerType, StringType, StructField, StructType}
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
      .schema(Schema.sample())//set schema. for prod environment. setting schema is recommended
      .schema(Schema.sampleDDL())//set schema. for prod environment. setting schema is recommended
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

  /**
   * spark-submit할 때, 데이터베이스의 jdbc 드라이버 jar파일을 설정해야함
   * --driver-class-path postgresql-9.4.1207.jar --jars postgresql-9.4.1207.jar
   * @return
   */
  def getJdbcDataFrame(): DataFrame = {
    val DB_URL = "jdbc:mysql://your-mysql-server-url.com"
    val DATABASE, TABLE, USERNAME, PASSWORD = ""

    spark.read.format("jdbc")
      .option("url", DB_URL)
      .option("dbtable", s"$DATABASE.$TABLE")

      //pushdownQuery, spark의 모든 함수를 지원하지는 못한다. 지원이 안될 경우,
      // 데이터베이스에서 모든 데이터를 가져와서 spark내에서 처리하므로 비효율적. 이 경우, 테이블 쿼리를 직접 입력
      .option("dbtable", s"(select distinct(value) from table_name) as table_name")
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

    // 컬럼이 하나인 경우.
    Seq((1,), (2,), (3,)).toDF("value") //버전에 따라 에러 나는듯?
    Seq(Tuple1(1), Tuple1(2), Tuple1(3))

    //or
    val rows = Seq(Row(1), Row(2), Row(3))
    val rdd = spark.sparkContext.parallelize(rows)
    spark.createDataFrame(rdd, Schema.sample())
  }

  def createDataFrameByRow(spark: SparkSession) = {
    val rdd = spark.sparkContext.parallelize(Seq(Row(1, 2, "string1" ),
      Row(2, 3, "string2" ),
      Row(4, 5, "string3" )))
    val struct = StructType(Array(
      StructField("aa", IntegerType, true),
      StructField("bb", IntegerType, false),
      StructField("bb", StringType, false)
    ))
    spark.createDataFrame(rdd, struct)
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

  def range() = {
    spark.range(10e4.toLong)
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
      .option("inferSchema", "true")//이걸 추론하기 위해서, 데이터를 읽고, 그로인해, csv파일 용량이 크면, action이 수행 되기 전에, dataframe을 만드는 것도 시간이 오래 걸릴 수 있음.
      .option("mode", "FAILFAST")//wrong format, then terminate directly. default : PERMISSIVE : null로 설정하고, _corrupt_record라는 컬럼에 기록.
      .csv("s3://hyun/aaa.csv")
  }

  def getUrl() = {
    import org.apache.commons.io.IOUtils
    import java.net.URL
    import java.nio.charset.Charset
    val bankText = spark.sparkContext.parallelize(
      IOUtils.toString(
        new URL("https://s3.amazonaws.com/apache-zeppelin/tutorial/bank/bank.csv"),
        Charset.forName("utf8")).split("\n"))

    bankText.toDF("value")
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
    spark.read
      .option("mergeSchema", "true")
      .parquet("path")
  }

}
