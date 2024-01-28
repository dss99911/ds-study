package spark.stream

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.col
import za.co.absa.abris.avro.functions.from_avro
import za.co.absa.abris.config.AbrisConfig

/**
 * topic : 카테고리
 * record : 키, 값, 타임스탬프로 구성.
 * offset : 레코드 위치
 * subscribe : 데이터를 읽는 동작
 * publish : 데이터 쓰는 동작
 *
 * assign : 토픽뿐만아니라, 읽으려는 파티션까지 세밀하게 지정 {"topicA"[0,1], "topicB":[2,4]}
 * subscribe, subscribePattern : 데이터 읽기, 패턴 지정 가능.
 *
 * https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html
 *
 * --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,
 *
 * error handling patterns
 * https://www.confluent.io/blog/error-handling-patterns-in-kafka/
 */
class StreamingKafka {
  def readFromKafka(spark: SparkSession): DataFrame = {
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


    spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "kafka1.some.com:9092,kafka2.some.com:9092,kafka3.some.com:9092")
      .option("subscribe", "topic_name")
      .option("kafka.group.id", "some_name")

      //Offset fetching
      //https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#offset-fetching
      //todo 공부 필요
      .option("spark.sql.streaming.kafka.useDeprecatedOffsetFetching", value=false)

      //Consumer Caching
      // https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#consumer-caching
      .option("spark.kafka.consumer.cache.capacity", 64)
      .option("spark.kafka.consumer.cache.timeout", "5m")

      .option("startingOffsets", "latest") //가장 최근 offset부터 시작 "latest" for streaming,
      .option("startingOffsets", "earliest") // "earliest" for batch

      //이 갯수보다 커지면, trigger시점에 이 이상은 읽지 않음. 처리속도가 느리면, kafka에 추가되는 데이터보다, 더 적은 데이터를 처리하게 되어. offset 차이가 많이 날 수 있음
      //StreamingQueryListener의 numInputRows의 갯수가 항상 max를 기록하는지로 확인이 가능할 듯
      .option("maxOffsetsPerTrigger", 10000)

      .option("minPartitions", 100)//읽을 때, 파티션 갯수. 이것에 따라, kafka에서 각 partition별로 데이터 사이즈를 조절한다고..
      .load()
  }

  /**
   * 장점 :  스키마를 미리 설정하여, 올바른 데이터가 전달되는지 파이프라인 단에서 확인이 가능.
   *        안전하게 스키마 변경 가능.
   *        kafka에서 데이터를 받을때 스키마 정보 없이 받는다고 함. json과 비교해서, 상대적으로 적은 용량의 데이터 전달
   * 단점 :  Schema Registry 의 장애가 발생하는 경우 정상적으로 메시지를 전달하지 못하게 됨
   *        Avro 포맷은 JSON등과 비교하여 직렬화과정에서 퍼포먼스가 조금 떨어진다
   * https://medium.com/@gaemi/kafka-%EC%99%80-confluent-schema-registry-%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%9C-%EC%8A%A4%ED%82%A4%EB%A7%88-%EA%B4%80%EB%A6%AC-1-cdf8c99d2c5c
   *
   * --repositories https://packages.confluent.io/maven/
   * --packages org.apache.spark:spark-avro_2.12:3.1.2,io.confluent:kafka-schema-registry-client:5.5.0,io.confluent:kafka-avro-serializer:5.5.0,za.co.absa:abris_2.12:4.2.0
   */
  def schemaRegistry(spark: SparkSession) = {
    def getAbrisConfig() = {
      AbrisConfig
        .fromConfluentAvro
        .downloadReaderSchemaByLatestVersion
        .andTopicNameStrategy("topic1")
        .usingSchemaRegistry("SCHEMAREGISTRY_URL")
    }

    val abrisConfig = getAbrisConfig()

    val deserialized = readFromKafka(spark)
      .select(from_avro(col("value"), abrisConfig).as("obj")).select("obj.*")
  }

  def writeToKafka(spark: SparkSession) = {
    readFromKafka(spark).selectExpr("topic", "CAST(key AS STRING)", "CAST(value AS STRING)")
      .writeStream.format("kafka")
      .option("checkpointLocation", "/to/HDFS-compatible/dir")
      .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
      .start()
  }
}
