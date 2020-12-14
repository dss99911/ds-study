
object Maps {

  var ratings = Map(
    "Lady in the Water"  -> 3.0,
    "Snakes on a Plane"  -> 4.0,
    "You, Me and Dupree" -> 3.5
  )

  // how to transform Map values
  ratings.transform((k, v) => v + 1)

  for ((name,rating) <- ratings) println(s"Movie: $name, Rating: $rating")
  ratings.foreach {
    case(movie, rating) => println(s"key: $movie, value: $rating")
  }
  val tuple: (String, Double) = "ddf" -> 3.0
  ratings += "ddf" -> 3.0
  ratings ++= Map(tuple, "ddf" -> 3.0)//for mutable
  ratings --= List("ddf", "ddf")//for mutable
  ratings -= "ddf"

  val states = collection.mutable.Map("AK" -> "Alaska")
  states("ddsf") = "dd"//able to set value when use mutable.map
  private val optional: Option[String] = states.get("ddd")
  states.contains("dsfasdf")

  val aa = ratings ++ Map("ddf" -> 3.0, "ddf" -> 3.0)
}
