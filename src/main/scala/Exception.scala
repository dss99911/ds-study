import java.io.{FileNotFoundException, IOException}

import scala.util.{Failure, Success, Try}

object Exception {
  try {
    //
  } catch {
    case fnfe: FileNotFoundException => println(fnfe)
    case ioe: IOException => println(ioe)
    case _: Throwable => println("dd")
  } finally {

  }

  def toInt(s: String): Try[Int] = Try {
    Integer.parseInt(s.trim)
  }
  toInt("dd") match {
    case Success(i) => println(i)
    case Failure(s) => println(s"Failed. Reason: $s")
  }

  val y = for {//y is Success or Failure
    a <- toInt("1")
    b <- toInt("d")
    c <- toInt("d")
  } yield a + b + c

}
