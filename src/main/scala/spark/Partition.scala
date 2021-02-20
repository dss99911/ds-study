package spark

import org.apache.spark.sql.SparkSession

/**
 * https://medium.com/@mrpowers/managing-spark-partitions-with-coalesce-and-repartition-4050c57ad5c4
 *
 * - when load, spark doesn't change partition count to fit the data size. so, even if data is filtered much, partition count is same.
 *    so, repartitioning is better for the case,
 * - decide coalesce or repartition as both as each difference. check the url
 * - Spark tries to set the number of partitions automatically based on your cluster.(so, no need to set partition normal case)
 */
class Partition {
  val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._

  //show partition size
  Read.getParquetDataFrame().rdd.partitions.size
  Read.getParquetDataFrame().rdd.getNumPartitions

  //save data on 1 partition
  Read.getParquetDataFrame().coalesce(1)

  //The repartition algorithm does a full shuffle of the data and creates equal sized partitions of data.
  Read.getParquetDataFrame().repartition(Cluster.getCpuCount() * 4)// recommended count of partition is 2~4 https://stackoverflow.com/questions/35800795/number-of-partitions-in-rdd-and-performance-in-spark/35804407#35804407

  //coalesce combines existing partitions to avoid a full shuffle. so it may not be 6 partition but can be less
  //coalesce doesn't increase partition count. but move rows between existing partition. so, if set count more than current. it keep current count
  Read.getParquetDataFrame().coalesce(6)


  //특정 파티션으로 분할해서 저장하는 경우, repartition도 해주고, partitionBy도 해주면, 성능이 더 향상되는 듯하다.(원인도 모르고, 확실하지도 않음. 하지만, repartition했더니, 2시간 되서, 처리 안되던게, 20분에 끝남)
  //참고 : https://stackoverflow.com/a/44810607/4352506
  Read.getParquetDataFrame().repartition($"key").write.partitionBy("key").parquet("/location")

}
