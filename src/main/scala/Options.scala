object Options {
  //Option have Some or None
  def toInt(s: String): Option[Int] = {
    try {
      Some(Integer.parseInt(s.trim))
    } catch {
      case e: Exception => None
    }
  }

  toInt("dsf") match {
    case Some(i) => println(i)
    case None => println("That didn't work.")
  }

  //able to use foreach. consiter Option as stream
  toInt("1").foreach(println)

  /**
   * If all three strings convert to integers, y will be a Some[Int], i.e., an integer wrapped inside a Some
   * If any of the three strings can’t be converted to an inside, y will be a None
   */
  val y = for {
    a <- toInt("1")
    b <- toInt("a")
    c <- toInt("c")
  } yield a + b + c

  //nullable field
  val santa = new Address(
    "1 Main Street",
    None,
    "North Pole",
    "Alaska",
    "99705"
  )

  //if use java.lang.Double. and if it's null.
  val d: java.lang.Double = null
  val a = Option(d) // => Option of java.lang.Double. -> None
  new C(Option(d)) // => Option of scala.Double -> 0.0 (automatically changed to 0
  class C(val b: Option[Double])
}

class Address (
                var street1: String,
                var street2: Option[String],
                var city: String,
                var state: String,
                var zip: String
              )