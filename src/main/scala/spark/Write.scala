package spark

class Write {

  def writeParquet() = {
    Read.getParquetDataFrame().selectExpr("aid", "iid", "sdr", "msg", "mrt")
      .write
      .partitionBy("dt")
      .mode("overwrite")
      .parquet(s"s3://key")
  }
}
