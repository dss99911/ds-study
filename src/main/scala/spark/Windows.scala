package spark

import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.{dense_rank, max, nth_value, percent_rank, rank, row_number, sum, to_date, window}
import org.apache.spark.sql.types.TimestampType

/**
 * rowsBetween
 * - Window.unboundedPreceding : indicates that the window starts at the first row of the partition
 * - Window.currentRow : indicates the window begins or ends at the current row
 * - Window.unboundedFollowing : indicates that the window ends at the last row of the partition
 * -
 */
class Windows {
  val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()
  df.drop()
    df.withColumn("num",
      row_number.over(
        //window 범위 설정
        Window
          .partitionBy("pattern_id", "error_message")
          .orderBy("pattern_id", "error_message")

          //default
          //  - orderBy가 있으면, 처음부터 현재 row까지
          //  - orderBy가 없으면, 처음부터 끝까지
          // 현재 row를 기준으로 +,- 범위 설정
          .rowsBetween(Window.unboundedPreceding, Window.currentRow)
      )
    )

  def window_functions() = {
    row_number()//frame내에서 순서(공통된 값이 있어도, 정렬된 순서에 따라 숫자가 정해짐
    rank()//공동1등이 있으면, 둘다 1이 되고, 그 다음은 3임.
    dense_rank()//공통1등이 있으면, 둘다 1이 되고, 그 다음은 2임.
    nth_value($"col_name", 5)//window에서 몇번째 row
    percent_rank() // percentile 형식으로 rank를 매김. 0, 0.5, 1 이런식으로. percentile로 seg를 구분할 때 사용.
  }

  def getFirstRowOfGroup() = {
    import org.apache.spark.sql.SaveMode
    import org.apache.spark.sql.expressions.Window

    val w = Window.partitionBy("type").orderBy("type")
    df.withColumn("rn", row_number.over(w))
      .where($"rn" === 1).drop("rn")
      .write
      .mode(SaveMode.Overwrite)
      .parquet("s3://hyun/temp/test")
  }

  def aggregateColumnByGroup() = {
    val w = Window.partitionBy("name").orderBy($"date".desc)
    Seq(
      ("a", "2021-05-20"),
      ("a", "2021-05-21"),
      ("a", "2021-05-22"),
      ("a", "2021-05-23"),
      ("b", "2021-04-20"),
      ("b", "2021-04-21"),
      ("b", "2021-04-22"),
      ("b", "2021-04-23")
    ).toDF("name", "date")
      .withColumn("date", to_date($"date"))
      .withColumn("last_time", max($"date").over(w))
      .show()
  }

  def groupByDateRange() = {
    val a = Seq(System.currentTimeMillis() / 1000,2,3,4,5)

    a.toDF().withColumn("date", $"value".cast(TimestampType))
      .groupBy(window($"date", "1 day"))
      .count()

      .show(truncate = false)

    //    [1970-01-01 00:00:00, 1970-01-02 00:00:00]	4
    //    [2021-02-17 00:00:00, 2021-02-18 00:00:00]	1
  }

  def cumulate() = {
    //value로 오름차순해서, 누적 합계를 보여준다.
    df.withColumn("cum_sum", sum("value").over(Window.orderBy("value")))
  }

  def totalSumCumSum() = {
//    val w_group = Window.partitionBy("group").orderBy($"count".desc)
    val w_from_first_to_current = Window.partitionBy("group").orderBy($"count".desc)
      .rowsBetween(Window.unboundedPreceding, Window.currentRow)

    df
      //todo check bug reason :if use same partitionBy column on different window. only last window is reflected.
//      .withColumn("total_count_over_group", sum($"count").over(w_group))
      .withColumn("cum_count_over_group", sum($"count").over(w_from_first_to_current))
  }
}
