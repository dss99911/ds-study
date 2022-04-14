import org.apache.spark.sql
import org.apache.spark.sql.functions.col

object Functions {
  def varArgs(text: String*) = {

  }

  def returnArray(): Array[String] = {
    Array("a", "b")
  }

  def returnTuple(): (String, Int) = {
    ("a", 1)
  }

  val Array(a, b) = returnArray()
  val (c: String, d) = returnTuple()

}


object ExtensionFunction {
  implicit class Extension(text: String) {
    def sampleText(): String = {
      text.toLowerCase
    }
  }

  //If same scope, you can use extension function directly
  def example() = {
    "TTT".sampleText()
  }
}

class A {
  //If different scope, you have to add importAA._
  import ExtensionFunction._
  "dsaf".sampleText()
}