
/**
 * similar with data class in Kotlin
 * automatically generate copy method, equal, hashcode, toString
 */
class CaseClass {


  trait P {
    def name: String
  }

  case class Student(name: String, year: Int) extends P
  case class Teacher(name: String, specialty: String) extends P

  def getPrintableString(p: Person): String = p match {
    case Student(name, year) =>
      s"$name is a student in Year $year."
    case Teacher(name, whatTheyTeach) =>
      s"$name teaches $whatTheyTeach."
  }
}
