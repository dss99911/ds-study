class Objects {
  //using companion object
  val p2: Person = Person("Regina")
  val p3: Person = Person(Some("Regina"), Some(1))
  Person.apply("dd")//the above is same with this
}

object Person {
  def apply(name: String): Person = {
    new Person(name)
  }

  // a two-arg constructor
  def apply(name: Option[String], age: Option[Int]): Person = {
    new Person(name.get)
  }
}