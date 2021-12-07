package spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.col

/**
 * https://luminousmen.com/post/the-5-minute-guide-to-using-bucketing-in-pyspark
 * https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-bucketing.html
 * https://mathjhshin.github.io/Spark%EC%97%90%EC%84%9C%EC%9D%98-Bucketing/
 *
 * partitioning한 컬럼의 값이 user_id처럼 다양하면, partition이 너무 많이 발생하게 되고, 이게 오히려, 성능저하를 야기할 수 있다.
 * 이럴때 bucketing을 사용함.
 *
 * join시 특정 shuffle을 방지하는 목적도 있음
 *
 * shuffle 방지 목적
 *
 * 사용 예
 * - id로 조인하는 경우, id로 partition을 나누면 파티션이 너무 많이 만들어지고, 파티션별로 폴더가 생성된다.
 * - 이 경우, id로 bucketing하면, sortMergeJoin등에서 shuffle이 일어나지 않는다.
 *
 *
 * no exchange query가 되기 위한 조건
 * - The number of partitions on both sides of a join has to be exactly the same. (파티션 수 주의)
 * - Both join operators have to use HashPartitioning partitioning scheme. (broadcast join이면 안됨)
 *    - spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
 * - partition과 bucket을 동시에 사용하는 경우, bucket_id만 가지고 join해야 됨. partition과 bucket을 같이 하면 안됨.(이유 모름)
 *
 */
class Bucketing {
  private val spark: SparkSession = SparkSessions.createSparkSession()
  val t1 = spark.table("unbucketed1")
  val t2 = spark.table("unbucketed2")

  t1.join(t2, "key").explain()
  /*
  this shows Exchange hashpartitioning. because "key" is not partitioned. so need shuffle
  == Physical Plan ==
*(5) Project [key#10L, value#11, value#15]
+- *(5) SortMergeJoin [key#10L], [key#14L], Inner
   :- *(2) Sort [key#10L ASC NULLS FIRST], false, 0
   :  +- Exchange hashpartitioning(key#10L, 200)
   :     +- *(1) Project [key#10L, value#11]
   :        +- *(1) Filter isnotnull(key#10L)
   :           +- *(1) FileScan parquet default.unbucketed1[key#10L,value#11] Batched: true, Format: Parquet, Location: InMemoryFileIndex[file:/opt/spark/spark-warehouse/unbucketed1], PartitionFilters: [], PushedFilters: [IsNotNull(key)], ReadSchema: struct<key:bigint,value:double>
   +- *(4) Sort [key#14L ASC NULLS FIRST], false, 0
      +- Exchange hashpartitioning(key#14L, 200)
         +- *(3) Project [key#14L, value#15]
            +- *(3) Filter isnotnull(key#14L)
               +- *(3) FileScan parquet default.unbucketed2[key#14L,value#15] Batched: true, Format: Parquet, Location: InMemoryFileIndex[file:/opt/spark/spark-warehouse/unbucketed2], PartitionFilters: [], PushedFilters: [IsNotNull(key)], ReadSchema: struct<key:bigint,value:double>, SelectedBucketsCount: 16 out of 16
   */

  t1
    .repartition(16, col("key"))// repartition안하고, overwrite하면 file exists 에러가 남?
    .write
    .bucketBy(16, "key")//partitionBy도 설정할 수 있음. 하지만, bucketBy의 컬럼과 겹치면 안됨. parition dynamic overwrite 사용하면 bucketBy의 컬럼에는 적용안됨.
    .sortBy("value")//생략 가능
    .saveAsTable("bucketed")

  val t3 = spark.table("bucketed")
  val t4 = spark.table("bucketed")
  t3.join(t4, "key").explain()
  /*
  No exchange is shown
  == Physical Plan ==
*(3) Project [key#14L, value#15, value#30]
+- *(3) SortMergeJoin [key#14L], [key#29L], Inner
   :- *(1) Sort [key#14L ASC NULLS FIRST], false, 0
   :  +- *(1) Project [key#14L, value#15]
   :     +- *(1) Filter isnotnull(key#14L)
   :        +- *(1) FileScan parquet default.bucketed[key#14L,value#15] Batched: true, Format: Parquet, Location: InMemoryFileIndex[file:/opt/spark/spark-warehouse/bucketed], PartitionFilters: [], PushedFilters: [IsNotNull(key)], ReadSchema: struct<key:bigint,value:double>, SelectedBucketsCount: 16 out of 16
   +- *(2) Sort [key#29L ASC NULLS FIRST], false, 0
      +- *(2) Project [key#29L, value#30]
         +- *(2) Filter isnotnull(key#29L)
            +- *(2) FileScan parquet default.bucketed[key#29L,value#30] Batched: true, Format: Parquet, Location: InMemoryFileIndex[file:/opt/spark-warehouse/bucketed], PartitionFilters: [], PushedFilters: [IsNotNull(key)], ReadSchema: struct<key:bigint,value:double>, SelectedBucketsCount: 16 out of 16
   */
}
