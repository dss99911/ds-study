package spark.stream

import org.apache.spark.sql.streaming.StreamingQueryListener.{QueryProgressEvent, QueryStartedEvent, QueryTerminatedEvent}
import org.apache.spark.sql.streaming.{OutputMode, StreamingQueryListener, Trigger}
import org.apache.spark.sql.{DataFrame, Dataset, ForeachWriter, SaveMode, SparkSession}
import spark.SparkSessions

import java.util.concurrent.TimeUnit

/**
 * Source : 입력 스트림
 * Sink : 출력 스트
 * Trigger : 데이터를 싱크로 출력하는 시점 제어
 */
class Streaming {

  def createSparkSession() = {
    SparkSession
      .builder()
      .master("yarn")
      .config("spark.streaming.stopGracefullyOnShutdown", true) //현재 처리하고 있는 배치를 전부 처리 후 종료.
      .config("spark.eventLog.enabled", false) //오래 수행 되기 때문에, log를 저장하면, 데이터 저장소가 부족해질수도 있을 듯.
      .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
      .getOrCreate()
  }
  /**
   * this is for test only. socket connection on driver node
   * nc -lk 9999 로 소켓을 생성하여, 테스트 데이터 전달 가능
   */
  def readFromSocket(spark: SparkSession) = {
    spark.readStream.format("socket")
      .option("host", "localhost")
      .option("port", 9999)
      .load()
  }

  /**
   * 파일 소듯
   * 파일이 새로 생성될 때마다, 불러오기 때문에, 완성된 파일만 소스 디렉토리에 저장되어야함.(파일에 append를 하면 안됨)
   * @param spark
   * @return
   */
  def readFromJson(spark: SparkSession) = {
    spark.conf.set("spark.sql.shuffle.partitions", 5)//for local testing

    val static = spark.read.json("data/activity-data/")
    val dataSchema = static.schema
    val streaming = spark.readStream.schema(dataSchema)
      .option("maxFilesPerTrigger", 1)//한 트리거당 최대 처리할 파일 수
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

    //micro-batch mode에서만 작동한다고 함. trigger가 continuous가 아닌 경우.
    readFromJson(spark).as[String].writeStream.foreachBatch((batchDf: Dataset[String], batchId: Long) => {

    })
  }

  /**
   * 집계 후, 싱크를 덮어씌울 경우 사용.
   * 맵 연산만 하는 경우 complete 모드 사용 불가
   *
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
   * 워터마크와 이벤트시간을 이용하면, 집계한 결과만 append가능하게 할 수 있음.
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
   * 싱크가 저수준 업데이트를 지원해야 한다고함.
   * 집계 후, 변경된 row만 싱크에 출력됨.
   * 집계를 안하면, append와 동일
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

  def writeFile(spark: SparkSession) = {
    readFromJson(spark)
      .writeStream
      .foreachBatch((batchDF: DataFrame, batchId: Long) => {
        batchDF.write
          .mode(SaveMode.Append)
          .parquet("s3://bucket/aa")
        println("result count : " + batchDF.count())
      })
  }

  def useTrigger(spark: SparkSession) = {
    //ProcessingTime : write periodically
    readFromJson(spark).writeStream.trigger(Trigger.ProcessingTime("5 seconds"))
    readFromJson(spark).writeStream.trigger(Trigger.ProcessingTime(1, TimeUnit.DAYS))//kafka의 경우, max.poll.interval.ms 보다 길면 안됨.(카프카 캐시때문일듯..?)

    //테스트시에는 한번에 처리가능한 분량을 스트리밍에서 테스트하는데 사용.
    //실제 사용시에는 단발성 update를 하고 싶을 때, batch코드를 작성하지 않고, streaming코드로 배치 처리가 가능.
    readFromJson(spark).writeStream.trigger(Trigger.Once())
  }

  /**
   * 장애시, 재시작으로 장애 해소.
   * HDFS, S3 등에 checkpoint 저장
   * 현재 트리거에서 처리한 오프셋 범위 정보, 중간 상태값을 저장
   * 장애가 난 경우, 버그 픽스 후, 장애가 난 지점부터 다시 시작할 수 있다고 함(하지만, 중대한 변화가 이러난 경우에는 checkpoint directory를 사용할 수 없다는 에러 발생한다고함)
   */
  def checkPointLocation(spark: SparkSession) = {
    readFromJson(spark).writeStream
      .option("checkpointLocation", "/some/location/")
  }

  def dropDuplicate(spark: SparkSession) = {
    readFromJson(spark)
      .withWatermark("event_time", "5 hours")//without watermark. all data is kept on memory when using groupBy
      .dropDuplicates("user", "event_time")
      .groupBy("user")
      .count()
  }

  def size() = {
    SparkSessions.createSparkSession().streams.active
    //check when stream is running.
    //check on same server by http server
    // so, it seems that it should call on same spark application running
  }

  def checkStream(spark: SparkSession) = {
    println(spark.streams.active)

    for( i <- 1 to 5 ) {
      spark.sql("SELECT * FROM activity_counts").show()
      Thread.sleep(1000)
    }
  }

  def monitoring(spark: SparkSession) = {
    val query = readFromJson(spark).writeStream.start()
    query.status // current status. like the below
    // {
    //    "message" : "Getting offsets from...",
    //    "isDataAvailable" : true,
    //    "isTriggerActive" : true
    //  }
    query.recentProgress// 아래와 같은 상황을 알 수 있음
    //numInputRows : 780119,
    //processedRowsPerSecond : 19779,
    //durationMs : {
    //  addBatch : 38179,
    //  getBatch : 235,
    //  getOffset : 518,
    //  queryPlanning : 138,
    //  triggerExecution : 39440
    //  walCommit : 312
    //}
    //stateOperators [ {
    //  numRowsTotal : 7,
    //  numRowsUpdated : 7
    // } ]
    //sources,
    //sink

    query.recentProgress

    spark.streams.addListener(new StreamingQueryListener() {

      override def onQueryStarted(event: QueryStartedEvent): Unit = {}

      override def onQueryTerminated(event: QueryTerminatedEvent): Unit = {}

      override def onQueryProgress(event: QueryProgressEvent): Unit = {
        println(event.progress.prettyJson)
        //connect to prometeus or grafana
        //UDP seems better?
      }
    })

  }

  def stopSteraming(spark: SparkSession) = {
    //todo need to check if this is proper way or not.
    // this is used for stop streaming and restart directly daily by http web server api
    if(spark.streams.active.length > 0) {
      spark.streams.active.foreach(s => {
        s.stop()
      })
    }
  }

  def performance() = {
    //udf이후 filter를 하면, 성능이 급격히 하락하는 사례가 있었음.
  }
}
