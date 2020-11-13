import scala.collection.mutable.ArrayBuffer

object Classes {
  val p: Person = new Person("Regina", "dd")
}

class Person(var firstName: String, var lastName: String) {
  //def and field or any code is processed same way
  println("the constructor begins")

  def printFullName() = println(s"$firstName $lastName")
}

abstract class Pet (name: String) {
  def speak(): Unit = println("Yo")   // concrete implementation
  def comeToMaster(): Unit            // abstract method
}

class Dog(name: String) extends Pet(name) {
  override def speak() = println("Woof")
  def comeToMaster() = println("Here I come!")
}

class Pizza (
              var crustSize: CrustSize,
              var crustType: CrustType,
              val toppings: ArrayBuffer[Topping] = new ArrayBuffer() //like ArrayList in Java
            ) {
  // one-arg auxiliary constructor
  def this(crustType: CrustType) = {
    this(SmallCrustSize, crustSize = crustType)
  }

  // zero-arg auxiliary constructor
  def this() = {
    this(RegularCrustType)
  }

  def addTopping(t: Topping): Unit = toppings += t
  def removeTopping(t: Topping): Unit = toppings -= t
  def removeAllToppings(): Unit = toppings.clear()

  def test = {
    val p2 = new Pizza(ThickCrustType)
    val p4 = new Pizza
  }
}


sealed trait Topping
case object Cheese extends Topping
case object Pepperoni extends Topping
case object Sausage extends Topping
case object Mushrooms extends Topping
case object Onions extends Topping

sealed trait CrustSize
case object SmallCrustSize extends CrustSize
case object MediumCrustSize extends CrustSize
case object LargeCrustSize extends CrustSize

sealed trait CrustType
case object RegularCrustType extends CrustType
case object ThinCrustType extends CrustType
case object ThickCrustType extends CrustType
