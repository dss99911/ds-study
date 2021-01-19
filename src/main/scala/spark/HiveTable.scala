package spark

import org.apache.spark.sql.SparkSession

class Sql {
  //http://jason-heo.github.io/programming/2017/02/17/parquet-to-hive-table.html
  import org.apache.spark.sql.DataFrame

  //need enableHiveSupport
  val sc = SparkSessions.createSparkSession()

  val schema_info = sc.read.parquet("/path/to/_common_metadata")

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
