package spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.window

/**
 * https://kjhov195.github.io/2019-11-16-structured_streaming_3/
 * - window, slide, waterpark
 *
 * watermark
 * - without watermark. all data is kept on memory when using window or groupBy
 * - 워터마크 threshold까지 window들을 유지하여, 데이터 갱신함.
 * - todo 워터마크 유효기간 이후에 온 데이터는 그냥 무시하게 되는 건지? 아니면, 새로운 윈도우가 생성되는 건지? 새로운 윈도우가 생성되면, write할 때, 기존 집계데이터를 덮어씌을 수도있으므로 확인이 필요할듯..?
 */
class StreamingWindow {
  /**
   * 10분마다 트리거가 발생함.
   */
  def windowOnly(spark: SparkSession) = {
    import spark.implicits._
    new Streaming().readFromJson(spark)
      .withWatermark("event_time", "5 hours")
      .groupBy(window($"event_time", "10 minutes"))
  }

  /**
   * 5분마다 트리거가 발생하고, window범위는 10분임(겹치는 시간대 존재)
   */
  def windowAndSlide(spark: SparkSession) = {
    import spark.implicits._
    new Streaming().readFromJson(spark)
      .withWatermark("event_time", "5 hours")//without watermark. all data is kept on memory when using window
      .groupBy(window($"event_time", "10 minutes", "5 minutes"))
  }

  /**
   * TODO 각 그룹별로, 임의의 윈도우를 정의하고, 윈도우의 타임아웃인 워터마크를 제어할 수 있음.
   */
  def windowCustomState(spark: SparkSession) = {
    import spark.implicits._
    new Streaming().readFromJson(spark).groupByKey(_.getString(1))
//      .mapGroupsWithState()
//      .flatMapGroupsWithState()

  }
}
