package spark

import org.apache.spark.sql.SaveMode
import spark.Read.spark

class Write {
  import spark.implicits._
  def writeParquet() = {
    Read.getParquetDataFrame().selectExpr("aid", "iid", "sdr", "msg", "mrt")
      .write
      .partitionBy("dt")// overwrite할 경우, 전체에 대해서 overwrite하는게 아니라, 해당 파티션에 대해서만, overwrite함
      .mode("overwrite")
      .mode(SaveMode.Overwrite)
      .parquet(s"s3://key")
  }

  def writeSingleTextToFile() = {
    //save json to file
        val str = "some data"
        List(str)
          .toDS().rdd
          .coalesce(1)
          .saveAsTextFile("somePath")
  }

  def writeCsv() = {
    Read.getParquetDataFrame()
      .coalesce(1)
      .write
      .option("header","true")
      .csv("path")
  }
}
