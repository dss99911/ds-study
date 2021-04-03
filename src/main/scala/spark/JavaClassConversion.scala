package spark

import com.fasterxml.jackson.databind.ObjectMapper
import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.functions.{col, collect_list, from_json, schema_of_json, struct}

import java.text.SimpleDateFormat
import java.util
import scala.collection.mutable

/**
 * recommended to use Scala class.
 * or define same scala class with java class
 */
class JavaClassConversion {
  val spark = SparkSessions.createSparkSession()
  import spark.implicits._
  //make JavaClass able to be serialized

  val frame = (1 to 100)
    .toDF("value")
    .withColumn("ten", $"value" % 10)

  //convert rows to java class
  implicit val javaClassEncoder = org.apache.spark.sql.Encoders.kryo[JavaClass]
  frame.map(r => r.json)
    .map(r => new ObjectMapper()
      //if contains Timestamp, consider format
      .setDateFormat(new SimpleDateFormat("yyyy-MM-dd hh:mm:ss"))
      .readValue(r, classOf[JavaClass]))

  //convert java class to row
  // schema_of_json is not recommended. as schema can be different.
  // so, it's better to define same class on scala
    .map(r => new ObjectMapper().writeValueAsString(r))
    .toDF("json")
  frame
    .withColumn("obj", from_json($"json", schema_of_json(frame.as[String].first())))
    .drop("json")
    .select("obj.*")
    .show()

  //convert list struct to java class
  import scala.collection.JavaConverters._
  implicit val listEncoder = org.apache.spark.sql.Encoders.kryo[util.List[JavaClass]]
  val frame2 = (1 to 100)
    .toDF("value")
    .withColumn("ten", $"value" % 10)
  frame2
    .groupBy($"ten")
    .agg(collect_list(struct(frame2.columns.map(col):_*)).as("list"))
    .select("ten", "list")
    .map{ r =>
      val mapper = new ObjectMapper()
      r.getAs[mutable.WrappedArray.ofRef[Row]](1)
      .map(v => mapper.readValue(v.json, classOf[JavaClass])).asJava
    }
    .map(r => r.asScala.map(_.ten))
}
