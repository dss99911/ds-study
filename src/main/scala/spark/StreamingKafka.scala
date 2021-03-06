package spark

import org.apache.spark.sql.SparkSession

/**
 * topic : 카테고리
 * record : 키, 값, 타임스탬프로 구성.
 * offset : 레코드 위치
 * subscribe : 데이터를 읽는 동작
 * publish : 데이터 쓰는 동작
 *
 * assign : 토픽뿐만아니라, 읽으려는 파티션까지 세밀하게 지정 {"topicA"[0,1], "topicB":[2,4]}
 * subscribe, subscribePattern : 데이터 읽기, 패턴 지정 가능.
 */
class StreamingKafka {
  def readFromKafka(spark: SparkSession) = {
    // Subscribe to 1 topic
    val ds1 = spark.readStream.format("kafka")
      .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
      .option("subscribe", "topic1")
      .load()
    // Subscribe to multiple topics
    val ds2 = spark.readStream.format("kafka")
      .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
      .option("subscribe", "topic1,topic2")
      .load()
    // Subscribe to a pattern of topics
    val ds3 = spark.readStream.format("kafka")
      .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
      .option("subscribePattern", "topic.*")
      .load()
    ds3
  }

  def writeToKafka(spark: SparkSession) = {
    readFromKafka(spark).selectExpr("topic", "CAST(key AS STRING)", "CAST(value AS STRING)")
      .writeStream.format("kafka")
      .option("checkpointLocation", "/to/HDFS-compatible/dir")
      .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
      .start()
  }
}
