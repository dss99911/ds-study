import scala.collection.mutable

object HelloWorld extends App {
  println("Hello, World!")

  EnumObj.values.foreach {
    case d if (d == EnumObj.first) => println("d")
    case _ => None
  }
  println(EnumObj.first)
}

//can use this way as well
//object Hello {
//  def main(args: Array[String]) = {
//    println("Hello, world")
//  }
//}