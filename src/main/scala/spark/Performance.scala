package spark

/**
 * UDF vs map vs custom spark native : https://medium.com/@fqaiser94/udfs-vs-map-vs-custom-spark-native-functions-91ab2c154b44
 */
class Performance {
  /**
   * can see how to process the data in physical side
   * == Physical Plan ==
   * *(1) SerializeFromObject [assertnotnull(input[0, $line60.$read$$iw$$iw$foo, true]).id AS id#894L, assertnotnull(input[0, $line60.$read$$iw$$iw$foo, true]).addOne AS addOne#895L]
   * +- *(1) MapElements <function1>, obj#893: $line60.$read$$iw$$iw$foo
   * +- *(1) DeserializeToObject createexternalrow(id#0L, StructField(id,LongType,false)), obj#892: org.apache.spark.sql.Row
   * +- *(1) InMemoryTableScan [id#0L]
   * +- InMemoryRelation [id#0L], StorageLevel(disk, memory, deserialized, 1 replicas)
   * +- *(1) Range (0, 10000000, step=1, splits=4)
   */
  Read.getParquetDataFrame().explain
  Read.getParquetDataFrame().explain(true)

  /**
   * DAGScheduler
   *    converts logical execution plan (i.e. RDD lineage of dependencies built using RDD transformations)
   *    to physical execution plan (using stages)
   *
   * To show RDD Lineage (logical execution plan)
   * res8: String =
(3) MapPartitionsRDD[11] at rdd at <console>:29 []
 |  SQLExecutionRDD[10] at rdd at <console>:29 []
 |  MapPartitionsRDD[9] at rdd at <console>:29 []
 |  ShuffledRowRDD[8] at rdd at <console>:29 []
 +-(2) MapPartitionsRDD[7] at rdd at <console>:29 []
    |  MapPartitionsRDD[6] at rdd at <console>:29 []
    |  MapPartitionsRDD[5] at rdd at <console>:29 []
    |  ParallelCollectionRDD[4] at rdd at <console>:29 []
   */
  Read.getParquetDataFrame().rdd.toDebugString

}
