package spark

import org.apache.spark.sql.types.{LongType, Metadata, StringType, StructField, StructType}

object StructTypes {
  def sample() = {
    StructType(Array(
      StructField("aa", StringType, true),
      StructField("bb", LongType, false, Metadata.fromJson("{\"hello\":\"world\"}"))
    ))
  }


}
