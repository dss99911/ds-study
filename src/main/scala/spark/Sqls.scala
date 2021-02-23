package spark

import org.apache.spark.sql.SparkSession

/**
 * hive sql engine은 일반 sql구문을 분산처리 시스템에서 돌아갈 수 있도록 변환해줌.
 * spark는 hive sql engine을 대체하여, sql구문을 분산처리 시스템에서 돌아갈 수 있게 해주어, hive를 대체하는 개념이지만, hive meta store는 spark와 같이 사용할 수 있음.
 * sql()을 호출하면, spark engine이 이 hive meta store를 참조하여, 처리를 한다(spark와 hive meta store를 어떻게 연동하는진 공부 필요할듯(AWS Glue를 공부하면 알 수 있을))
 * AWS Glue가 Hive metastore를 사용하고, sql()호출시, hive metastore를 통해, 데이터를 가져옴
 */
class Sqls {
  //http://jason-heo.github.io/programming/2017/02/17/parquet-to-hive-table.html
  import org.apache.spark.sql.DataFrame

  //need enableHiveSupport
  val spark = SparkSessions.createSparkSession()

  def createTableFromFile(filePath: String, tableName: String) = {
    val schema_info = spark.read.parquet(filePath)
    val col_definition = (for (c <- schema_info.dtypes) yield(c._1 + " " + c._2.replace("Type",""))).mkString(", ")

    /**
     * hive metastore에 table을 만들고, table과 실제 데이터의 path와 연결시킴.
     */
    //todo what is external meaning?
    val createStmt =s"""CREATE EXTERNAL TABLE ${tableName}
                 (
                    ${col_definition}
                 ) STORED AS PARQUET LOCATION '$filePath'"""

    spark.sql(createStmt)
  }
  createTableFromFile("/path/to/_common_metadata", "my_table")


  /**
   * if table is updated from external.
   * spark sql may cache the table. so, need to update the table
   */
  def refreshTable() = {
    spark.catalog.refreshTable("my_table")

    //테이블과 관련된 모든 캐싱항목을 갱신한다고 함.
    //todo 어떤 캐싱을 말하는 거고, 어떤 케이스인지 잘 모르겠음
    spark.sql("REFRESH table table_name")

    //수동으로 신규파티션을 만들 경우, 테이블을 수리해야 한다고 함.
    //그런데, spark를 통해서 신규 파티션을 만들 경우에는 필요 없지 않을까?
    //읽는 관점에서는 다른곳에서 spark로 신규 파티션을 만든 경우도 수동으로 신규파티션을 만든 걸로 이해해야하나?
    //todo 다른 곳에서 spark로 신규 파티션을 만든 경우, 파티션이 자동 갱신되는지 확인 필요
    // 외부 테이블의 경우, drop table을 해도, 해당 table은 삭제되지 않고, 다만 해당 데이터를 table명으로 참조를 못한다고..
    spark.sql("MSCK REPAIR TABLE table_name")
  }

  /**
   * todo check the difference between 'stored' 'using' phrase
   * @return
   */
  def usingPhrase() = {
    spark.sql("""CREATE TABLE flights (fields...) USING JSON OPTIONS (path 'some/path') """)

    //make table from other table with some condition
    spark.sql("""CREATE TABLE flights (fields...) USING parquet AS SELECT * from flights """)

  }

  def create() = {
    //파티션 분리된 테이블 생성
    spark.sql("CREATE TABLE some_table USING parquet PARTITIONED BY (col_name) AS SELECT col_name, other_col, count FROM other_table LIMIT 5")
  }

  def insert() = {

    //특정 파티션에만 쓰고 싶은 경우.
    spark.sql(
      """INSERT INTO table_name
        |PARTITION (country="KOREA")
        |SELECT count, country from origin_table_name
        |WHERE country="KOREA" limit 12
        |""".stripMargin)
  }

  def dropTable = {
    spark.sql("DROP TABLE table_name;")
    spark.sql("DROP TABLE IF EXISTS table_name;")
  }

  def showTableInfo() = {
    spark.sql("DESCRIBE TABLE some_table")
    spark.sql("SHOW PARTITIONS some_table")//shows partition info
  }

  /**
   */
  def cache() = {
    spark.sql("CACHE TABLE some_table")
    spark.sql("UNCACHE TABLE some_table")
  }

  def corelatioQuery() = {
    // 내부 쿼리아ㅔ서 외부 쿼리의 컬럼 값을 참조 할 수 있음
    spark.sql(
      """
        |SELECT * FROM flights f1
        |WHERE EXISTS (SELECT 1 FROM flights f2
        |             WHERE f1.dest_country_name = f2.origin_country_name)
        |AND EXISTS (SELECT 1 FROM flights f2
        |             WHERE f2.dest_country_name = f1.origin_country_name)
        |""".stripMargin)

    //도중에 별도의 쿼리 추가
    spark.sql(
      """
        |select *, (select max(count) from flights) as maximum from flights
        |""".stripMargin)
  }
}


