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
    .option("path", "s3://bucket/tmp/tmp1") //path를 지정안하면, managed table can't be created because of path already exists에러가 발생하는 경우도 있음.
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

  def bigdata_bucket() = {
    /**
     * bucketing table 스캔하는데, 시간이 너무 오래 걸림
        - join보다는 filter가 그나마 빠름
        - 하나의 버캣을 체크하는데, 하나의 executor만 사용되는 것 같음. daily배치처럼 여러 bucket에서 사용하는게 많을 경우에는 병렬로 처리 되겠으나, 하나의 id만 불러오는 경우, 오래 걸림.
        - bucketing prune이 잘 되어, 하나의 버캣만 체크하는 것은 잘 되나, 시간이 오래 걸리는 이유가 현재 bucket에 저장 방식이 append이고, 파일을 너무 많이 형성되어, 하나의 버켓내에서도 파일을 많이 체크해야 하는 문제가 있어서 그런 것은 아닌가 생각됨.
            - 파일이 너무 많아지면, driver program의 메모리 증가하여, OOM발생할 수 있고, spark.driver.maxResultSize 가 부족해지는 현상 발생
            - delta + bucketing 은 discussion 중으로, 어려울 듯 https://github.com/delta-io/delta/issues/524
        - id별로 별도의 디렉토리를 만들어 보는 건 어떨까? (x)
            - 파일이 분산되는 건 delta 써서 머지하는 것도 고려
            - 저장이 너무 오래 걸림.
        - cardinarity가 높은 컬럼으로 bucketing하는 경우. 일반 database사용 고려. index나, key value지원 되는 것.
     */
  }

  def get_bucket_count(df: DataFrame) = {
     //https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-bucketing.html
      df.rdd.getNumPartitions
      //두 제플린에서 재시작 후 실행했는데도 때, 다른 결과값이 나오는 경우가 있음..
      //desc extended에는 bucket수 정확히 나옴
  }
}
