import java.lang

import scala.collection.JavaConverters.asJavaIterableConverter

class JavaCompatibility {
  private val ints: Array[Int] = Array(1, 2)
  private val list: List[Int] = ints.toList
  private val java: lang.Iterable[Int] = list.asJava
}