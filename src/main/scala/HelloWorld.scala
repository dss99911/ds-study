import scala.collection.mutable

object HelloWorld extends App {
  for (i <- 10 to 0 by -1) {
    println(i)
  }
}

//can use this way as well
//object Hello {
//  def main(args: Array[String]) = {
//    println("Hello, world")
//  }
//}