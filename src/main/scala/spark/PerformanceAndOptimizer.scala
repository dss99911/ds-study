package spark

/**
 * UDF vs map vs custom spark native : https://medium.com/@fqaiser94/udfs-vs-map-vs-custom-spark-native-functions-91ab2c154b44
 */
class PerformanceAndOptimizer {
  /**
   * can see how to process the data in physical side
   * 파티션 수도 나옴. splits등
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


  Read.getParquetDataFrame().queryExecution.executedPlan //직접 실행한 것처럼 로그가 찍힘. zeppelin처럼 로그가 안찍히는 경우 안 보임.
  Read.getParquetDataFrame().queryExecution.executedPlan.numberedTreeString //직접 실행한 것처럼 로그가 찍힘. zeppelin처럼 로그가 안찍히는 경우 안 보임.
  Read.getParquetDataFrame().queryExecution.toRdd.getNumPartitions // 버캣 갯수등, 파티션 수를 알 수 있음

  def partitionPrune() = {
    //파티션 prune이 제대로 되는지 확인하기.
    //FileSourceStrategy 로그에 prune여부가 찍힘(zeppelin에서는 로그가 안 보이기 때문에, spark-shell 등에서 실행해야 함)
    import org.apache.spark.sql.execution.datasources.FileSourceStrategy
    val logger = FileSourceStrategy.getClass.getName.replace("$", "")
    import org.apache.log4j.{Level, Logger}
    Logger.getLogger(logger).setLevel(Level.INFO)

    Read.getParquetDataFrame().filter("partition_id = 'a'").queryExecution.executedPlan

  }

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

  /**
   * https://spark.apache.org/docs/3.0.0-preview/sql-ref-syntax-aux-analyze-table.html
   *
   * todo ANALYZE TABLE students COMPUTE STATISTICS  을 하면,
   *  비용기반 옵티마이저가 작동하는 건지?
   *  analyze table을 실행 안 하면 작동안하는 건지?
   *  Analyze를 하는 것도 비용인데,
   *  analyze는 언제 호출 하는게 비용 측면에서 좋은 건지?
   *  조인 전에 analyze를 하는게 좋다고 하는데??
   */
  def optimizeByStatistics() = {
    val spark = SparkSessions.createSparkSession()
    spark.sql("ANALYZE TABLE table_name COMPUTE STATISTICS")
    spark.sql(
      """
        |ANALYZE TABLE table_name COMPUTE STATISTICS FOR
        |COLUMNS column_name1, column_name2, ...
        |""".stripMargin)

    //Show Statistics
    spark.sql("DESC EXTENDED table_name")
    /*
Type	EXTERNAL
Provider	hive
Statistics	43357165203 bytes, 126496099 rows
Location	s3://linked_path
Serde Library	org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe
InputFormat	org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat
OutputFormat	org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat
Storage Properties	[serialization.format=1]
Partition Provider	Catalog

     */
  }

}
