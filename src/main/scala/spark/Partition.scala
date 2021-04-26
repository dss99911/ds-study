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
  //파티션 갯수에 따라, 저장되는 파일 갯수가 다름
  //한 파일당 용량이 너무 크면 안좋음
  //coalesce를 filter 후에 적용해도, filter 하기전에 하나의 파티션으로 모든 데이터를 모으게되는 사례가 있음,
  // repartition은 filtering한 결과를 하나의 파티션으로 모은다고 함.
  // filtering에서 제거되는 데이터가 많다면, repartition이 더 효과적일 수 있음
  Read.getParquetDataFrame().coalesce(1)

  //The repartition algorithm does a full shuffle of the data and creates equal sized partitions of data.
  Read.getParquetDataFrame().repartition(Cluster.getCpuCount() * 4)// recommended count of partition is 2~4 https://stackoverflow.com/questions/35800795/number-of-partitions-in-rdd-and-performance-in-spark/35804407#35804407

  //coalesce combines existing partitions to avoid a full shuffle. so it may not be 6 partition but can be less
  //coalesce doesn't increase partition count. but move rows between existing partition. so, if set count more than current. it keep current count
  Read.getParquetDataFrame().coalesce(6)


  //특정 파티션으로 분할해서 저장하는 경우, repartition도 해주고, partitionBy도 해주면, 성능이 더 향상되는 듯하다.(원인도 모르고, 확실하지도 않음. 하지만, repartition했더니, 2시간 되서, 처리 안되던게, 20분에 끝남)
  // 생각되는 이유 : repartition없이 partitionBy를 하면, 실제로 partition 분할 없이 worker node에 데이터들이 분산되어 있는데, 이걸 저장할 때만 파티션 분할을 하게 되어서, 병렬로 저장을 못해서 그런 것 같음
  //             그래서, partitionBy를 한다고해서, executor들에 데이터들이 분산된 후 처리되지는 않고, 저장시에만 분산되어 저장됨.
  //참고 : https://stackoverflow.com/a/44810607/4352506
  Read.getParquetDataFrame().repartition($"key").write.partitionBy("key").parquet("/location")


  //id로 파티션을 나눠야 하는 경우, id는 유저별로 값이 다 달라서, 오버헤드가 엄청 크다. 특히 파일에 파티션별로 저장하는 경우에
  //그래서 prefix등으로 크게 묶어서 저장하고, 검색시에, prefix + id로 검색하기도 한다.
  Read.getParquetDataFrame()
    .filter($"andid_prefix" === "121" && $"androidId" === "121123213123")
}
