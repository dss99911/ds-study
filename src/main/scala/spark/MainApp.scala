package spark

import org.apache.spark.sql.SparkSession

/**
 * Note that applications should define a main() method instead of extending scala.App. Subclasses of scala.App may not work correctly.
 * (https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications)
 */
object MainApp {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder
      //some case, there is error. https://stackoverflow.com/questions/52133731/how-to-solve-cant-assign-requested-address-service-sparkdriver-failed-after
      .config("spark.driver.host", "127.0.0.1")
      .appName("Simple Application")
      .getOrCreate()

    new Statistics().summary(spark)

  }

}
