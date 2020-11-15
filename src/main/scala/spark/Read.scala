package spark

import org.apache.spark.sql.{DataFrame, Dataset, SparkSession}

object Read {
  val spark: SparkSession = SparkSessionCreate.createSparkSession()
  import spark.implicits._

  def getParquetDataFrame(): DataFrame = {
    spark.read.parquet("s3://text")
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
