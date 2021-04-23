package spark

import org.apache.spark.sql.types.{LongType, Metadata, StringType, StructField, StructType}

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
