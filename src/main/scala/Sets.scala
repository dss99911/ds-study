import scala.collection.mutable

class Sets {
//https://docs.scala-lang.org/overviews/scala-book/set-class.html
  val a = mutable.Set[String]()
  val b = Set[String]()

  a += "d"
  a += "e"
  a.contains("b")

}
