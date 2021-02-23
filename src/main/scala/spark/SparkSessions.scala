package spark

import org.apache.spark.sql.SparkSession

object SparkSessions {
  def createSparkSession(): SparkSession = {
    val spark = SparkSession.builder.appName("acs_tx_extractor")
      .enableHiveSupport()//TODO check when it's used. udf를 쓰기 위해서 인지? 아니면 partitionBy 메서드를 쓰기 위해서 인지. https://stackoverflow.com/a/52170175/4352506
      .getOrCreate()

    //available to overwrite specific partition only
    //without this, when overwriting, all partition is deleted and save new partition.
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    //default is 200. if it's local mode. it doesn't need many partition.
    //조인 등을 통해 셔플이 일어나면, default로 200개의 파티션/task 생성됨
    spark.conf.set("spark.sql.shuffle.partitions", "5")

    spark
  }

  def version() = {
    createSparkSession().version
  }
}
