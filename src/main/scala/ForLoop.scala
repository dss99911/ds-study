
object ForLoop {
  val args = List("apple", "banana", "lime", "orange")
  val names = List("apple", "banana", "lime", "orange")
  val tuples = List(("apple","apple"), ("apple","apple"))

  for (arg <- args) println(arg)

  //0, 1, 2, 3, 4, 5
  for (i <- 0 to 5) println(i)

  //0, 1, 2, 3, 4
  for (i <- 0 until 5) println(i)

  // "x to y by" syntax
  for (i <- 0 to 10 by 2) println(i)

  // from 10 to 0
  for (i <- 10 to 0 by -1) println(i)

  // yield makes collection
  val x = for (i <- 1 to 5) yield i * 2

  val capNames = for (name <- names) yield {
    val nameWithoutUnderscore = name.drop(1)
    val capName = nameWithoutUnderscore.capitalize
    capName
  }

  tuples.foreach{
    case (x,y) => println(x + " " + y)
  }
}
