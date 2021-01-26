package spark

import org.apache.spark.sql.SparkSession

/**
 * hive sql engine은 일반 sql구문을 분산처리 시스템에서 돌아갈 수 있도록 변환해줌.
 * spark는 hive sql engine을 대체하여, sql구문을 분산처리 시스템에서 돌아갈 수 있게 해주어, hive를 대체하는 개념이지만, hive meta store는 spark와 같이 사용할 수 있음.
 * sql()을 호출하면, spark engine이 이 hive meta store를 참조하여, 처리를 한다(spark와 hive meta store를 어떻게 연동하는진 공부 필요할듯(AWS Glue를 공부하면 알 수 있을))
 * AWS Glue가 Hive metastore를 사용하고, sql()호출시, hive metastore를 통해, 데이터를 가져옴
 */
class HiveTable {
  //http://jason-heo.github.io/programming/2017/02/17/parquet-to-hive-table.html
  import org.apache.spark.sql.DataFrame

  //need enableHiveSupport
  val sc = SparkSessions.createSparkSession()

  val schema_info = sc.read.parquet("/path/to/_common_metadata")

  /**
   * hive metastore에 table을 만들고, table과 실제 데이터의 path와 연결시킴.
   */
  def get_create_stmt(table_name : String, schema_info : DataFrame) : String = {
    val col_definition = (for (c <- schema_info.dtypes) yield(c._1 + " " + c._2.replace("Type",""))).mkString(", ")

    var create_stmt = s"""CREATE EXTERNAL TABLE ${table_name}
                 (
                    ${col_definition}
                 ) STORED AS PARQUET LOCATION '/path/to/'"""

    create_stmt
  }

  // CREATE EXTERNAL TABLE ...
  val create_stmt = get_create_stmt("my_tab", schema_info)

  sc.sql(create_stmt)
}


