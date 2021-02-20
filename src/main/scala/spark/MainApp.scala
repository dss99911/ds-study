package spark

import org.apache.spark.sql.SparkSession

/**
 * Note that applications should define a main() method instead of extending scala.App. Subclasses of scala.App may not work correctly.
 * (https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications)
 */
object MainApp {
  def main(args: Array[String]): Unit = {
    StructuredStream.readSocket()
  }
}
