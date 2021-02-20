package spark

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.streaming.OutputMode
import org.apache.spark.sql.types.StructType

object StructuredStream {
  /**
   * when test. run socket on port 9999 with 'nc -lk'
   */
  def readSocket() = {
    val spark = SparkSession
      .builder
      .appName("StructuredNetworkWordCount")
      .getOrCreate()

    import spark.implicits._

    // Create DataFrame representing the stream of input lines from connection to localhost:9999
    val lines = spark.readStream
      .format("socket")
      .option("host", "localhost")
      .option("port", 9999)
      .load()

    // Split the lines into words
    val words = lines.as[String].flatMap(_.split(" "))

    // Generate running word count
    val wordCounts = words.groupBy("value").count()

    writeInMemory(wordCounts)
  }

  def readCsvFiles() = {
    val spark = SparkSession
      .builder
      .appName("StructuredNetworkWordCount")
      .getOrCreate()

    // Read all the csv files written atomically in a directory
    val userSchema = new StructType().add("name", "string").add("age", "integer")
    val csvDF = spark
      .readStream
      .option("sep", ";")
      .schema(userSchema)      // Specify schema of the csv files
      .csv("/path/to/directory")    // Equivalent to format("csv").load("/path/to/directory")
  }

  def writeConsole(df: DataFrame) = {
    // Start running the query that prints the running counts to the console
    val query = df.writeStream
      .outputMode(OutputMode.Complete())
      .format("console")
      .start()
    query.awaitTermination()
  }
  def writeInMemory(df: DataFrame) = {
    val query = df.writeStream
      .outputMode(OutputMode.Complete())
      .format("memory")
      .queryName("sample")
      .start()
    query.awaitTermination()
  }
}
