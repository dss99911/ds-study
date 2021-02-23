package spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, udf}

/**
 * https://wikidocs.net/29410
 */
object Udfs {
  private val spark: SparkSession = SparkSessions.createSparkSession()

  def some_func(text: String): String = {
    ""
  }

  //use directly.
  val random = udf(() => Math.random())
  val someFunc = udf((text: String) => some_func(text))
  val someFunc2 = udf(some_func(_: String): String)
  val someFunc3 = udf(some_func(_: String))

  //use for sql, so, register udf on spark context.
  //if use distributed cluster, direct way may not work. in that cse use 'register'
  spark.udf.register("random", random.asNondeterministic())
  spark.udf.register("some_func", some_func _) //for adding function need '_'
  spark.sql("SELECT random()").show()


  //one argument
  val plusOne = udf((x: Int) => x + 1)
  spark.udf.register("plusOne", plusOne)
  spark.sql("SELECT plusOne(5)").show()

  //two argument
  spark.udf.register("strLenScala", (_: String).length + (_: Int))//register without udf()
  spark.sql("SELECT strLenScala('test', 1)").show()


  // UDF in a WHERE clause
  spark.udf.register("oneArgFilter", (n: Int) => {
    n > 5
  })
  spark.range(1, 10).createOrReplaceTempView("test")
  spark.sql("SELECT * FROM test WHERE oneArgFilter(id)").show()

  Read.getListDataFrame()
    .withColumn("random", random())
    .withColumn("plusOne", plusOne(col("some")))

  //Hive UDF를 쓸 수도 있음. 정확히 어떻게 쓰는진 모름
  //enableHiveSupport()를 해줘야함
  //CREATE TEMPORARY FUNCTION myFunc As 'com.organization.hive.udf.FunctionName'
}
