package spark

import org.apache.spark.sql.SparkSession

/**
 * https://medium.com/@mrpowers/managing-spark-partitions-with-coalesce-and-repartition-4050c57ad5c4
 *
 * - when load, spark doesn't change partition count to fit the data size. so, even if data is filtered much, partition count is same.
 *    so, repartitioning is better for the case,
 * - decide coalesce or repartition as both as each difference. check the url
 * - Spark tries to set the number of partitions automatically based on your cluster.(so, no need to set partition normal case)
 *
 * 정렬 주의사항
  - 정렬 후에 repartition하면, 정렬이 파티션별로 섞이게됨.
  - repartition후에 정렬을 하면, partition갯수가 바뀔 수 있음
  - 파일을 하나만 만들면서, 정렬도 하고 싶다면, coalesce(1)를 하기
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
  //Coalesce를 하는 방식
  // - coalesce가 셔플을 하지 않게 하는 방식이, 애초에 upstream에서부터 파티션 갯수를 고정해서 셔플을 방지하는 것
  // - coalesce를 filter 후에 적용해도, filter 하기전에 하나의 파티션으로 데이터를 모아서 처리하여, filter가 많은 데이터를 제외 시킬 경우, 하나의 파티션에서 작업이 진행되기 때문에 속도가 느림
  // - coalesce가 아닌 repartition을 하게되면, upstream에서는 파티션 갯수가 자유로워, 병렬 처리 후, filtering한 결과를 하나의 파티션으로 모음
  // - filtering에서 제거되는 데이터가 많다면, repartition이 더 효과적일 수 있음
  //정렬이되어 있는 하나의 파일 만들기
  // - 위에서 설명했듯, repartition을 통해 성능개선이 될 수 있는데, repartition을 하게 되면, 정렬되어 있는 데이터도, 섞이게 됨.
  // - repartition후에 다시 정렬하게 될 경우, 파티션이 여러개로 늘어남.
  // - 그래서, cache를 해도 된다면, filter후에, cache()를하고, coalesce(1)를 통해 파티션을 하나로 고정 후, sort를 통해 정렬을 하면, 파일이 하나인 정렬된 데이터를 만들 수 있음
  // - cache후에 , count등의 액션을 호출해서, coalesce를 호출하기 전에, 캐시에서 데이터를 가져올 수 있게 하기.
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
