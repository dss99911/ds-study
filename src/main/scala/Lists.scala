import org.apache.spark.sql

import scala.collection.mutable.{ArrayBuffer, ListBuffer}

/**
 * Class	Description
    *ArrayBuffer	: an indexed, mutable sequence
    *ListBuffer	: mutable (similar with MutableList)
    *List :	a linear (linked list), immutable sequence
    *Vector :	an indexed, immutable sequence
    *Map	: the base Map (key/value pairs) class
    *Set	: the base Set class
 */
object Lists {
  def temp() = {
    val nums: List[Int] = List.range(0, 10)
    val nums2 = (1 to 10 by 2).toList
    val letters = ('a' to 'f').toList
    val letters2 = ('a' to 'f' by 2).toList
    val names2 = Array("joel", "ed", "chris", "maurice")
    val names = List("joel", "ed", "chris", "maurice")
    val nums3 = Seq(1,2,3)
    val nums4 = ArrayBuffer(1,2,3)
    var text = ListBuffer[String]()


    val list = 1 :: 2 :: 3 :: Nil // list: List[Int] = List(1, 2, 3)

    nums
      .filter(_ < 4)
      .map(_ * 2)
      .map(_.toString)
      .map((i: String) => s"i : $i")
      .map(i => s"i : $i")
      .foldLeft("")(_ + _)//1st : seed value, 2nd : fold
      .foreach(println)

    list.sum //_ + _을 의미

    list.product //_ * _ 을 의미

    list.reduce(_ * 2 * _)//결과 값과 입력값의 타입이 동일한 경우
    nums.foldLeft("Start : ")((d, v) => d + v + ", ")//결과 값이 입력값과 달라서, 초기 값이 필요한 경우.
    //Start : 0 ~ 10

    var nums_inmutable = 1 +: nums //prepend 1. recommended to use 'prepend' on list
    nums_inmutable = nums :+ 1 //append 1. if need to use 'append' recommended to use vector
    nums_inmutable = nums ++ Array(1,2) //append 1,2

    // add one element
    nums4 += 4
    text += "d"
    text = text :+ "d" // make new array

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

    //convert list to varargs. list: _*
    val folders = Seq((1 to 59).map(n => s"""$n"""): _*)
    //  nums4 :+ 1: _* // if want to merge list and make varagrs

    //list to string by join
    nums.mkString(",")

    //with index
    val listWithIndex = list.zipWithIndex

    //java list to scala list
    import scala.collection.JavaConverters._
    nums.asJava.asScala
  }



  def main(args: Array[String]): Unit = {
    var names2 = Array("joel", "ed", "chris", "maurice")
    print((names2 :+ "d").mkString(","))
  }
}

