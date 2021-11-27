import java.lang
import scala.collection.JavaConverters._
import scala.jdk.CollectionConverters._

class JavaCompatibility {
  private val ints: Array[Int] = Array(1, 2)
  private val list: List[Int] = ints.toList
  private val java: lang.Iterable[Int] = list.asJava //scala.collection.JavaConverters
  private val scala: Iterable[Int] = java.asScala //scala.jdk.CollectionConverters
}