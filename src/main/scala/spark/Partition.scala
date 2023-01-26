package spark

import org.apache.spark.sql.functions.{col, spark_partition_id}
import org.apache.spark.sql.{SaveMode, SparkSession}

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

  def makeSortedSingleFilePerPertition() = {
    spark.read.parquet("source_path")
      .sort($"count".desc)
      .coalesce(1)
      .write
      .partitionBy("user_id")
      .option("header","true")
      .mode(SaveMode.Overwrite)
      .csv("result_path")
  }

  /**
   * TODO 아직 테스트 못해봄.
   *  만약 된다면, 위의 방식처럼 이상하게 처리하지 않고, 성능도 더 좋을 것이기 때문에, 위에 방식은 지우기.
   */
  def makeSortedSingleFilePerPertition2() = {
    spark.read.parquet("source_path")
      .select( $"username", $"timestamp", $"activity" )
      .repartition(col("username"))
      .sortWithinPartitions(col("username"),col("timestamp")) // <-- both here
      .write
      .partitionBy("username")
      .mode(SaveMode.Overwrite)
      .option("header", "true")
      .option("delimiter", ",")
      .csv("/useractivity")
  }

  def withPartitionId() = {
    spark.read.parquet("source_path")
      .repartition(125)
      .withColumn("partitionId", spark_partition_id) // todo 125개로 리파티션해서, 0~124의 번호가 할당될 것으로 추정. 확인 필요
  }

  def partitionByCol() = {
    // 값범위가 파티션보다 많고, 값에 중복이 없는 경우
    //  - 파티션별 값 수가 대략 10% 정도 차이를 보임.
    
    // 값범위가 파티션보다 많고, 값의 수가 균일한 경우
    //  - 파티션별로 distinct한 값의 수가 다름. 수가 적은 경우와 많은 경우 차이가 3배 이상이 됨.

    // 값범위가 파티션보다 많고, 값이 한쪽으로 편향된 경우
    //  - 값이 편향되어 있다고 해서, 값이 적은 파티션에 더 많은 값이 할당되거나 하지 않음.
    //  - 값의 수가 균일한 경우와 동일한 분포의 'distinct한 값의 수'가 파티션에 할당됨.
    //  - 따라서, 편향되어 있는 값이 포함된 파티션에 데이터가 몰림

    //파티션 수가 distinct한 값 수보다 크게 설정한 경우, distinct한 값 수 만큼의 파티션이 생성됨.
    //동일 값이 여러 파티션으로 분리될 줄 알았는데, 그렇지 않음.

    // 편향으로 인해, 시간이 오래걸린다면, 파티션을 더 많이 분할해서, 쉬는 core가 없게 한다.

    val df = spark.read.parquet("source_path")
      .repartition(100, $"col_name")

    // partitionBy를 하면, 각 task가 task안에 있는 row들을 partition별로 저장하게 되어, 대략 task수 * task안의 partition수 만큼의 파일이 생성된다.
    // 데이터가 작으면, 작은 파일이 너무 많이 생성되는 것.
    // https://www.linkedin.com/pulse/apache-spark-small-file-problem-simple-advanced-solutions-garg

    // partition이 한개이면, 3개 파일이 생성
    df.repartition(3).write.partitionBy("e")

    // partition이 5개 미만이면, spark_partition_id 수가 정확히 일치하지 않는 현상이 있으면,
    //  예: repartition(2), repartition(4)=> spark_partition_id이 1개.
    //     repartition(3)-> spark_partition_id이 3개
    df.repartition(3)

  }

  //The repartition algorithm does a full shuffle of the data and creates equal sized partitions of data.
  Read.getParquetDataFrame().repartition(Cluster.getCpuCount() * 4)// recommended count of partition is 2~4 https://stackoverflow.com/questions/35800795/number-of-partitions-in-rdd-and-performance-in-spark/35804407#35804407
  //각 파티션별로 데이터 차이가 크고(애초에 저장된 데이터가 파티션별로 차이가 있거나, 필터링등의 작업으로 차이가 생김) , 처리해야하는게 많다면, 처리전에 repartition해주는게 좋음.
  //stage에서 min, max 테스크 차이가 크면, 파티션 갯수를 늘려서, 고르게 할당하는게 좋음. 하지만, 셔플에 들어가는 비용도 있으므로, 균형을 잘 잡는게 좋음

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


  /**
   * 기본설정은 true, false로 놓으면 partition prunning이 안됨.
   * 사용 이유는 테이블들의 파티션 컬럼이 key 일 경우, key가 glue metastore에서 예약어로 쓰이고 있어서 에러가 발생해서.
   * 그래서, key 컬럼이 없는 테이블에 한해서 spark.conf.set("spark.sql.hive.manageFilesourcePartitions", true) 를 사용
   * 아래와 같은 에러가 났는데, 관련이 있는지는 확실하지 않음
   * org.apache.hadoop.hive.metastore.api.InvalidObjectException: null (Service: AWSGlue; Status Code: 400; Error Code: InvalidInputException

   */
  spark.conf.set("spark.sql.hive.manageFilesourcePartitions", false)

}
