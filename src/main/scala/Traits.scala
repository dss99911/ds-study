/**
 * - it's extending multiple classes
 * - able to abstract
 */
object Traits extends Runner with Speaker {
  override def speak(): String = "Hyun"

  class BB
  def test() = {
    //mixing traits on the fly
    val a = new BB() with Runner
    a.startRunning()
  }
}

/**
 * able to define field. and also can change field
 */
trait Runner {
  var a: String = "d"
  def startRunning() {
    println("I’m running")
    a = "b"
  }
  def stopRunning(): Unit = println("Stopped running")
}

trait Speaker {
  def speak(): String  // has no body, so it’s abstract
}