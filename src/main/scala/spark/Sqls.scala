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
     * link파일처럼 연결만 시켜주는 역할. 그래서 삭제 해도, 실제 데이터에 영향을 미치지 않음
     *
     * Locationd을 입력하면, unmanaged table이라고하고, 입력안하면, managed table이라고 함.
     */
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
    //todo REFRESH table table_name 테이블과 관련된 모든 캐싱항목을 갱신한다고 함. 테이블 스키마 변경시에만 해당 되는건지? 아니면, 파티션 추가시에도? 그리고, spark에서 스키마 변경시에도 카탈로그에서 알 수 없으므로 refresh가 필요할 것 같은데, 캐싱을 하는 레벨은 카탈로그인 글루에서 하는건지? 아니면 스파크 어플리케이션? 아니면 sql쿼리는 아테나를 통해서 하니 아테나? 하이브는 여기서 무슨 역할을 하는거지?
    spark.sql("REFRESH table table_name")

    //수동으로 신규파티션을 만들 경우, 테이블을 수리해야 한다고 함.
    //그런데, spark를 통해서 신규 파티션을 만들 경우에는 필요 없지 않을까?
    //읽는 관점에서는 다른곳에서 spark로 신규 파티션을 만든 경우도 수동으로 신규파티션을 만든 걸로 이해해야하나?
    //todo MSCK REPAIR TABLE table_name (위와 비슷한 질문임) 수동으로 신규파티션을 만들경우 필요하다고 하는데, 스키마는 글루에서 관리되고 있고, 그러면, spark로 신규 파티션을 추가한 경우에는, 글루에서 신규 파티션이 추가됐는지 모르므로, 신규 파티션 추가될 때마다, 글루에서 알 수 있게 하기 위해 호출해주는 것인지? 글루는 하이브와 어떤 관계인지?
    spark.sql("MSCK REPAIR TABLE table_name")
  }

  /**
   * todo check the difference between 'stored' 'using' phrase
   *  Athena를 통해 create table할 때, using과 stored가 있는데, stored는 external, using은 실제 데이터를 가진 테이블을 만드는 건지?
   *  아래와같이 설명되어 있는데, 무슨말인지 모르겠음.
   *  using -> using data source (https://docs.databricks.com/spark/latest/spark-sql/language-manual/sql-ref-syntax-ddl-create-table-datasource.html)
   *  stored as -> using hive format (https://docs.databricks.com/spark/latest/spark-sql/language-manual/sql-ref-syntax-ddl-create-table-hiveformat.html)
   *
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
    spark.sql("DESC TABLE some_table")
    spark.sql("SHOW PARTITIONS some_table")//shows partition info

    spark.sql("DESCRIBE EXTENDED table_name")
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


