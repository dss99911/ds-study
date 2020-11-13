import scala.+:
import scala.collection.mutable.ArrayBuffer

/**
 * Class	Description
    *ArrayBuffer	: an indexed, mutable sequence
    *List :	a linear (linked list), immutable sequence
    *Vector :	an indexed, immutable sequence
    *Map	: the base Map (key/value pairs) class
    *Set	: the base Set class
 */
object Lists {

  val nums = List.range(0, 10)
  val nums2 = (1 to 10 by 2).toList
  val letters = ('a' to 'f').toList
  val letters2 = ('a' to 'f' by 2).toList
  val names = List("joel", "ed", "chris", "maurice")
  val nums3 = Seq(1,2,3)
  val nums4 = ArrayBuffer(1,2,3)

  val list = 1 :: 2 :: 3 :: Nil // list: List[Int] = List(1, 2, 3)

  nums
    .filter(_ < 4)
    .map(_ * 2)
    .map(_.toString)
    .map((i: String) => s"i : $i")
    .map(i => s"i : $i")
    .foldLeft("")(_ + _)//1st : seed value, 2nd : fold
    .foreach(println)

  list.sum//_ + _

  list.product//_ * _

  list.reduce(_ * 2 * _)

  var nums_inmutable = 1 +: nums //prepend 1. recommended to use 'prepend' on list
  nums_inmutable = nums :+ 1 //append 1. if need to use 'append' recommended to use vector
  nums_inmutable = nums :++ Array(1,2) //append 1,2
  nums_inmutable = nums ++ Array(1,2) //append 1,2

  // add one element
  nums4 += 4

  // add multiple elements
  nums4 += 5 += 6

  // add multiple elements from another collection
  nums4 ++= List(7, 8, 9)

  // remove one element
  nums4 -= 9

  // remove multiple elements
  nums4 -= 7 -= 8

  // remove multiple elements using another collection
  nums4 --= Array(5, 6)
}
