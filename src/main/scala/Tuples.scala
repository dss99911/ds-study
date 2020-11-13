object Tuples {
  val t = (11, "Eleven", new Person("Eleven"))
  t._1
  t._2
  t._3

  val (num, string, person) = (11, "Eleven", new Person("Eleven"))
}
