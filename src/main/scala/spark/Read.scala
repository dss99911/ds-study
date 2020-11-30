package spark

import org.apache.spark.sql.{DataFrame, Dataset, SparkSession}

object Read {
  val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._

  def getParquetDataFrame(): DataFrame = {
    spark.read.parquet("s3://text")
  }

  def getGlobPatternParquetDatFrame(): DataFrame = {
    //https://hadoop.apache.org/docs/r2.7.2/api/org/apache/hadoop/fs/FileSystem.html#globStatus(org.apache.hadoop.fs.Path)
    spark.read.parquet("s3://text/*/aa")
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

  def getListDataFrame() = {
    val list = (1 to 100).map(i => (i, s"val_$i"))
    list.toDF()
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
}
