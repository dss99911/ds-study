package spark

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.json.JsonMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import org.apache.spark.sql.{Column, DataFrame, SparkSession}
import org.apache.spark.sql.functions.{col, from_json, lit, schema_of_json}
import org.apache.spark.sql.types.{DecimalType, LongType, StringType, StructField, StructType}
import spark.Read.Person

class Json {
  val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._
  import collection.JavaConverters._

  val list = (1 to 100).map(i => Person("name", i))
  private val listDf: DataFrame = list.toDF()

  //make json string
//  val mapper = new ObjectMapper
  //if use Scala classes. the below have to be used.
  val mapper = JsonMapper.builder()
    .addModule(DefaultScalaModule)
    .build()
  listDf.map(x => mapper.writeValueAsString(x))

  //data from json
  private val df: DataFrame = Read.getParquetDataFrame()

  //https://stackoverflow.com/a/34069986/4352506
  private val assumedSchema = schema_of_json(lit(df.select($"json_data").as[String].first))
  df.withColumn("parsed_data", from_json(col("json_data"), assumedSchema))
  df.withColumn("parsed_data2", from_json(col("json_data"), Schema.jsonSchema))

  df
    .withColumn("received_date", col("parsed_data.date"))
    .withColumn("error", col("parsed_data.error"))
    .withColumn("id", col("parsed_data.id"))
    .withColumn("parse_result", col("parsed_data.result"))
    .withColumn("sequence", col("parsed_data.successData.sequence"))
    .withColumn("type", col("parsed_data.successData.type"))
    .withColumn("data", col("parsed_data.successData.data"))
    .withColumn("name", col("parsed_data.successData.name"))
    .withColumn("place", col("parsed_data.successData.place"))
}

object Schema {
  val jsonSchema =
    StructType(
      Array(
        StructField("date", LongType),
        StructField("errorMessage", StringType),
        StructField("successData",
          StructType(
            Array(
              StructField("place", StringType),
              StructField("map",
                StructType(
                  Array(
                    StructField("data",
                      StructType(
                        Array(
                          StructField("number", DecimalType(12, 2)),
                          StructField("name", StringType),
                        )
                      )
                    )
                  )
                )
              ),
              StructField("reason", StringType)
            )
          )
        )
      )
    )
}
