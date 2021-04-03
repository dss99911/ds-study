package spark

class Encoders {
  object MyEnum extends Enumeration {
    type MyEnum = Value
    val Hello, World = Value
  }

  case class MyData(field: String, other: MyEnum.Value)

  object MyDataEncoders {
    implicit def myDataEncoder: org.apache.spark.sql.Encoder[MyData] = {
      //this convert the object to bytes
      org.apache.spark.sql.Encoders.kryo[MyData]
    }
  }


  object EnumTest {
    //define on other object. and just import
    import MyDataEncoders._

    def main(args: Array[String]): Unit = {
      //use encoder directly.
      implicit val mapEncoder = org.apache.spark.sql.Encoders.kryo[Map[String, Any]]
    }
  }
}
