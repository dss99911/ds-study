package spark

import org.apache.spark.sql.{ForeachWriter, SparkSession}
import org.apache.spark.sql.streaming.OutputMode

/**
 * Source : 입력 스트림
 * Sink : 출력 스트
 * Trigger : 데이터를 싱크로 출력하는 시점
 */
class Streaming {

  /**
   * this is for test only. socket connection on driver node
   * nc -lk 9999 로 소켓을 생성하여, 테스트 데이터 전달 가능
   */
  def readFromSocket(spark: SparkSession) = {
    spark.readStream.format("socket")
      .option("host", "localhost").option("port", 9999).load()
  }
  def readFromJson(spark: SparkSession) = {
    import spark.implicits._
    spark.conf.set("spark.sql.shuffle.partitions", 5)//for local testing

    val static = spark.read.json("data/activity-data/")
    val dataSchema = static.schema
    val streaming = spark.readStream.schema(dataSchema)
      .option("maxFilesPerTrigger", 1)//한 트리거당 최대 처리할 파일 수 todo 트리거가 뭔지 확인 필요.
      .json("data/activity-data")

    streaming.groupBy("gt").count()
  }

  /**
   * test only.
   */
  def writeToInMemoryTable(spark: SparkSession) = {
    val activityQuery = readFromJson(spark).writeStream
      .queryName("table_name")
      .format("memory")
      .outputMode(OutputMode.Complete())
      .start()

    activityQuery.awaitTermination()
  }

  /**
   * test only.
   */
  def writeToConsole(spark: SparkSession) = {
    //write stream to console
    val activityQuery = readFromJson(spark)
      .writeStream
      .queryName("activity_counts")
      .format("console")
      .outputMode(OutputMode.Complete())
      .start()

    activityQuery.awaitTermination()
  }



  /**
   * control stream directly.
   * consider failure-tolerant, and process only one time
   * @param spark
   * @return
   */
  def foreachStream(spark: SparkSession) = {
    import spark.implicits._

    readFromJson(spark).as[String].writeStream.foreach(new ForeachWriter[String] {
      def open(partitionId: Long, version: Long): Boolean = {
        // open a database connection
        //todo 내고장성과 한번 처리를 보장하기 위해, parititonId, 와 version으로 무언가 체크해야 한다고 하는데, 이해가 잘 안감.
        return true
      }
      def process(record: String) = {
        // write string to connection
      }
      def close(errorOrNull: Throwable): Unit = {
        // close the connection
      }
    })
  }

  /**
   * 맵 연산만 하는 경우 complete 모드 사용 불가
   */
  def writeComplete(spark: SparkSession) = {
    //write stream to console
    val activityQuery = readFromJson(spark)
      .writeStream
      .queryName("activity_counts")
      .format("console")
      .outputMode(OutputMode.Complete())
      .start()

    activityQuery.awaitTermination()
  }

  /**
   * Aggregation not supported
   * TODO 집계를하려면, 워터마크와 이벤트시간을 이용하면 가능하다고함.
   */
  def writeAppend(spark: SparkSession) = {
    //write stream to console
    val activityQuery = readFromJson(spark)
      .writeStream
      .queryName("activity_counts")
      .format("console")
      .outputMode(OutputMode.Append())
      .start()

    activityQuery.awaitTermination()
  }

  /**
   * TODO 싱크가 저수준 업데이트를 지원해야 한다고함.
   */
  def writeUpdate(spark: SparkSession) = {
    //write stream to console
    val activityQuery = readFromJson(spark)
      .writeStream
      .queryName("activity_counts")
      .format("console")
      .outputMode(OutputMode.Update())
      .start()

    activityQuery.awaitTermination()
  }

  def size() = {
    SparkSessions.createSparkSession().streams.active
    //show active streams. but it shows 0 size. when I test.
    // so, it seems that it should call on same spark application running
  }

  def checkStream(spark: SparkSession) = {
    println(spark.streams.active)

    for( i <- 1 to 5 ) {
      spark.sql("SELECT * FROM activity_counts").show()
      Thread.sleep(1000)
    }
  }
}
