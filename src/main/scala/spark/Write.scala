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
    //특수문자가 들어가고 줄바꿈이 있는 메시지의 경우, 줄바꿈을 제대로 인식 못하는 경우가 있다.
    //parquet으로 저장 후, 이것을 pandas로 excel로 변환 하면, 엑셀 파일로 공유하려고 할 때, 이렇게 하면 에러가 없음.
    Read.getParquetDataFrame()
      .coalesce(1)
      .write
      .option("header","true")
      .csv("path")
  }
}
