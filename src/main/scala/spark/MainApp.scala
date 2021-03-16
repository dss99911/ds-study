package spark

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions.{explode, udf}
import org.apache.spark.sql.{Row, SparkSession}

/**
 * Note that applications should define a main() method instead of extending scala.App. Subclasses of scala.App may not work correctly.
 * (https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications)
 */
object MainApp {
  def main(args: Array[String]): Unit = {
    val logText = "sdafasdf" // Should be some file on your system
    Logger.getLogger("org").setLevel(Level.OFF)
    Logger.getLogger("akka").setLevel(Level.OFF)
    val spark = SparkSession.builder
      //some case, there is error. https://stackoverflow.com/questions/52133731/how-to-solve-cant-assign-requested-address-service-sparkdriver-failed-after
      .config("spark.driver.host", "127.0.0.1")
      .appName("Simple Application")
      .getOrCreate()

    import spark.implicits._

    new Streaming().writeAppend(spark)

  }

}
