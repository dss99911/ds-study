package spark

import org.apache.spark.sql.types.{LongType, Metadata, StringType, StructField, StructType}

/**
 * 스키마 추가시, type 안정성 뿐만 아니라, 어느정도 속도도 개선됨
 */
object Schema {
  def sample() = {
    StructType(Array(
      StructField("aa", StringType, true),
      StructField("bb", LongType, false, Metadata.fromJson("{\"hello\":\"world\"}"))
    ))
  }

  def sampleDDL()= {
    "a INT, b STRING, c DOUBLE"
  }

  def getSchemaDDLString() = {
    Read.getCsv().schema.toDDL
  }

}
