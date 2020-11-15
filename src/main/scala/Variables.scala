object Variables {
  //https://docs.scala-lang.org/overviews/scala-book/prelude-taste-of-scala.html
  val x = 1 //immutable
  var y = 0 //mutable

  val b: Byte = 1
  val x1: Int = 1
  val l: Long = 1
  val s2: Short = 1
  val d: Double = 2.0
  val f: Float = 3f
  var b2 = BigInt(1234567890)
  var b3 = BigDecimal(123456.789)
  val c = 'a'

  //with type
  val s: String = "a string"

  //class
  val p: Person = new Person("Regina")
  //using companion object
  val p2: Person = Person("Regina")
  Person.apply("dd")//the above is same with this
}