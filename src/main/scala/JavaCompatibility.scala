import java.{lang, util}

// able to change import name
import scala.util.{Try => Trying}

class JavaCompatibility {
  import collection.JavaConverters._
//  import scala.jdk.CollectionConverters._
  private val ints: Array[Int] = Array(1, 2)
  private val list: List[Int] = ints.toList
  private val javaList: util.List[Int] = list.asJava //scala.collection.JavaConverters
  private val scalaList: Iterable[Int] = javaList.asScala //scala.jdk.CollectionConverters


}