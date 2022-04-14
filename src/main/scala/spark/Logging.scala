package spark

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession

class Logging {
  lazy val spark: SparkSession = SparkSession.builder
    //some case, there is error. https://stackoverflow.com/questions/52133731/how-to-solve-cant-assign-requested-address-service-sparkdriver-failed-after
    .config("spark.driver.host", "127.0.0.1")
    .appName("Simple Application")
    .getOrCreate()

  //diable spark logs.
  Logger.getLogger("org").setLevel(Level.OFF)
  Logger.getLogger("akka").setLevel(Level.OFF)

  spark.sparkContext.setLogLevel("ERROR")
  spark.sparkContext.setLogLevel("ALL")
}
