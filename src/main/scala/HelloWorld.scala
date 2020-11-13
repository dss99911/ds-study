
object HelloWorld extends App {
  println("Hello, World!")

  List.range(0, 10)
    .filter(_ < 4)
    .foreach(println)


}

//can use this way as well
//object Hello {
//  def main(args: Array[String]) = {
//    println("Hello, world")
//  }
//}