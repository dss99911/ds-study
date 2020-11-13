object ForLoop {
  val args = List("apple", "banana", "lime", "orange")
  val names = List("apple", "banana", "lime", "orange")

  for (arg <- args) println(arg)

  // "x to y" syntax
  for (i <- 0 to 5) println(i)

  // "x to y by" syntax
  for (i <- 0 to 10 by 2) println(i)

  // yield makes collection
  val x = for (i <- 1 to 5) yield i * 2

  val capNames = for (name <- names) yield {
    val nameWithoutUnderscore = name.drop(1)
    val capName = nameWithoutUnderscore.capitalize
    capName
  }
}
