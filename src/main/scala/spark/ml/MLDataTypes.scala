package spark.ml

import org.apache.spark.sql.SparkSession

class MLDataTypes {

  /**
   * 비어있는 영역이 많고, 실제로 값이 있는 레이블이 제공됨
   */
  def getFromLibsvm(spark: SparkSession) = {
    spark.read.format("libsvm").load("path")
  }

}
