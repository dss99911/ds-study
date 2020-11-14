package spark

import spark.SparkSessionCreate.createSparkSession

class SqlCreate {
  def createTableFromCode = {
    val spark = createSparkSession()
    spark.range(1, 10).createOrReplaceTempView("test")

    spark.sql("SELECT * FROM test").show()
  }
}
