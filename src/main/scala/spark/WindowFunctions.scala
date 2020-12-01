package spark

import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.row_number

class WindowFunctions {
  private val df: DataFrame = Read.getParquetDataFrame()
    df.withColumn("rank",
      row_number().over(
        Window
          .partitionBy("pattern_id", "error_message")
          .orderBy("pattern_id", "error_message")))
}
