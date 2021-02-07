package spark

import org.apache.spark.broadcast

/**
 * copy data to each cluster.
 * and read-only.
 *
 * 특정 값이 여러 노드에 걸쳐서 사용될 경우.
 * 특정 값이 Job과 관련 없이 처음에 가져와서 지속적으로 사용될 경우
 * 특정 값이 어떤 task의 결과로서 존재하는데, 이 값이, 다음 task를 위한 데이터로만 존재하는게 아니라, 지속적으로 사용될 경우
 */
class Broadcast {
  val spark = SparkSessions.createSparkSession()
  private val data: broadcast.Broadcast[String] = spark.sparkContext.broadcast("1")

  data.value
}
