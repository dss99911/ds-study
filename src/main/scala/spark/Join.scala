package spark

import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.col

class Join {
  def join() = {
    //joinType default is inner, check comment on joinType on join method
    //'left', 'right'
    val s = Read.getParquetDataFrame().as("s")
    val c = Read.getParquetDataFrame().as("c")
    s.join(c, col("s.id") === col("c.id"))
      .select(
        col("s.id").alias("id"),
        col("c.code").alias("code"),
        col("s.text").alias("text")
      ).where("c.status = 1")
  }
}
