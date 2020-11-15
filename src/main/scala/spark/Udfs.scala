package spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, udf}

object Udfs {
  private val spark: SparkSession = SparkSessions.createSparkSession()
  val random = udf(() => Math.random())
  spark.udf.register("random", random.asNondeterministic())
  spark.sql("SELECT random()").show()


  //one argument
  val plusOne = udf((x: Int) => x + 1)
  spark.udf.register("plusOne", plusOne)
  spark.sql("SELECT plusOne(5)").show()

  //two argument
  spark.udf.register("strLenScala", (_: String).length + (_: Int))
  spark.sql("SELECT strLenScala('test', 1)").show()


  // UDF in a WHERE clause
  spark.udf.register("oneArgFilter", (n: Int) => { n > 5 })
  spark.range(1, 10).createOrReplaceTempView("test")
  spark.sql("SELECT * FROM test WHERE oneArgFilter(id)").show()

  Read.getListDataFrame()
    .withColumn("random", random())
    .withColumn("plusOne", plusOne(col("some")))
}
