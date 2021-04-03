package spark

import io.delta.tables.DeltaTable
import org.apache.hadoop.fs.Path
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.delta.DeltaTableUtils
import org.apache.spark.sql.functions.{desc, expr}

/**
 * https://www.youtube.com/watch?v=0eae1WHzMKU
 * 핵심 기능
 * - 데이터 변경에 대한 로그가 남음
 *    - git 처럼 데이터의 변경 히스토리가 남음,
 *    - snapshot 및 revert/rollback 할 수 있음.
 *    - reproduce도 할수 있다고 함.
 *    - audit에도 용이.
 * - 스키마 변경이 쉽다고 함.
 *  - 컬럼이 추가되면, 자동으로 스키마 변경하게 할 수도 있는듯. (https://docs.delta.io/latest/delta-batch.html#automatic-schema-update)
 *  - 스키마 교체 : https://docs.delta.io/latest/best-practices.html#replace-the-content-or-schema-of-a-table
 * - merge function
 *    - update
 *    - delete
 *    - upsert
 * 특징
 * - parquet으로 저장됨
 *
 * 기타
 * - convert delta table to parquet table
 * - convert parquet table to delta table
 *
 * 성능 튜닝 (https://docs.delta.io/latest/delta-update.html#performance-tuning)
 * - update, delete, upsert시의 condition에, parition key를 넣어주면, partition prune을 통해, 해당파티션에서만 체크함.
 * - compact files : 데이터 업데이트 할 때마다(특히 머지시.), 작은 파일들이 많이 생성된다고함. 그래서, 큰 파일로 만들어주는 repartition 이 필요함.
 *    - todo compact file은 작은 파일이 이미 많이 생겼을 때 하는 거 아닐까?, 아래의 두개만 잘 해도 되는 건 아닌지..?
 * - Control the shuffle partitions for writes
 * - Repartition output data before write
 *
 * 이슈
 * - spark submit할 때 --packages io.delta:delta-core_2.12:0.8.0 를 호출 해줘야함.
 */
class DeltaLake {
  val spark = SparkSession.builder.appName("BaseTransactionizer")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .enableHiveSupport().getOrCreate()
  import spark.implicits._

  def selectDelta() = {
    spark.read.format("delta").load("s3://delta-data")
  }

  def writeTable() = {
    selectDelta().write
      .format("delta")
      .save("/tmp/delta-table")
  }

  def update() = {
    // Update every even value by adding 100 to it
    val deltaTable = DeltaTable.forPath(spark, "s3://delta-data")
    deltaTable.update(
      condition = expr("id % 2 == 0"),
      set = Map("id" -> expr("id + 100")))

    // Delete every even value
    deltaTable.delete(condition = expr("id % 2 == 0"))
  }

  def upsertWithDelta() = {
    val newData = Read.getListDataFrame()

    DeltaTable.forPath(spark, "s3://delta-data")
      .as("old")
      .merge(
        newData.as("new"),
        "old.uniqueKey = new.uniqueKey")
      .whenMatched.updateAll()
      .whenNotMatched.insertAll()
      .execute()
  }

  def readOldVersion() = {
    val df = spark.read.format("delta").option("versionAsOf", 0).load("/tmp/delta-table")
    df.show()
  }

  def writeStreaming() = {
    val streamingDf = spark.readStream.format("rate").load()
    val stream = streamingDf
      .select($"value" as "id")
      .writeStream
      .format("delta")
      .option("checkpointLocation", "/tmp/checkpoint")
      .start("/tmp/delta-table")
  }

  def readStreaming() = {
    //todo update나 삭제시에는 어떻게 읽는 거지?
    val stream2 = spark.readStream.format("delta").load("/tmp/delta-table").writeStream.format("console").start()

  }


  def checkDeltaTable() = {
    //처음 테이블을 만들 때, delta table이 아니면, 델타 테이블을 만들고, 아니면, 업데이트 하게서 하기 위해
    DeltaTableUtils.isDeltaTable(spark, new Path("s3://delta-data"))
  }

  /**
   * https://docs.delta.io/latest/delta-utility.html#retrieve-delta-table-history
   */
  def getHistory() = {
    val deltaTable = DeltaTable.forPath(spark, "pathToTable")

    val fullHistoryDF = deltaTable.history()    // get the full history of the table
      .filter("operation = 'MERGE'")
      .orderBy(desc("version"))
      .select("version",
        "operationMetrics.numTargetRowsInserted",
        "operationMetrics.numTargetRowsUpdated"
      )
    val lastOperationDF = deltaTable.history(1) // get the last operation
  }
  /**
   * 기본적으로 30일의 commit을 저장함.
   * vacuum을 하면, default로 7일까지는 남기고, 이후의 것은 삭제함.
   * @return
   */
  def vaccumHistory() = {
    DeltaTable.forPath("s3://path").vacuum()
  }

  /**
   * Athena와 같은 곳에서 Delta table을 이용할 수 있게 하기 위해서 필요함.
   */
  def generateManifestFile() = {
    val deltaTable = DeltaTable.forPath("<path-to-delta-table>")
      deltaTable.generate("symlink_format_manifest")
  }

  /**
   * https://docs.delta.io/latest/best-practices.html#compact-files
   */
  def makeCompactFile() = {
    val path = "..."
    val numFiles = 16

    spark.read
      .format("delta")
      .load(path)
      .repartition(numFiles)
      .write
      .option("dataChange", "false")
      .format("delta")
      .mode("overwrite")
      .save(path)

    //특정 파티션만 repartition하기.
    val partition = "year = '2019'"
    val numFilesPerPartition = 16

    spark.read
      .format("delta")
      .load(path)
      .where(partition)
      .repartition(numFilesPerPartition)
      .write
      .option("dataChange", "false")
      .format("delta")
      .mode("overwrite")
      .option("replaceWhere", partition)
      .save(path)
  }
}
