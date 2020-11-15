package spark

/**
 * https://medium.com/@mrpowers/managing-spark-partitions-with-coalesce-and-repartition-4050c57ad5c4
 *
 * - when load, spark doesn't change partition count to fit the data size. so, even if data is filtered much, partition count is same.
 *    so, repartitioning is better for the case,
 * - decide coalesce or repartition as both as each difference. check the url
 * - Spark tries to set the number of partitions automatically based on your cluster.(so, no need to set partition normal case)
 */
class Partition {
  //show partition size
  Read.getParquetDataFrame().rdd.partitions.size

  //save data on 1 partition
  Read.getParquetDataFrame().coalesce(1)

  //The repartition algorithm does a full shuffle of the data and creates equal sized partitions of data.
  Read.getParquetDataFrame().repartition(Cluster.getCpuCount() * 4)// recommended count of partition is 2~4 https://stackoverflow.com/questions/35800795/number-of-partitions-in-rdd-and-performance-in-spark/35804407#35804407

  //coalesce combines existing partitions to avoid a full shuffle. so it may not be 6 partition but can be less
  //coalesce doesn't increate partition count. but move rows between existing partition. so, if set count more than current. it keep current count
  Read.getParquetDataFrame().coalesce(6)

}
