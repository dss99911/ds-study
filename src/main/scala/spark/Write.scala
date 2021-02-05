package spark

import spark.Read.spark

class Write {
  import spark.implicits._
  def writeParquet() = {
    Read.getParquetDataFrame().selectExpr("aid", "iid", "sdr", "msg", "mrt")
      .write
      .partitionBy("dt")
      .mode("overwrite")
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
}
