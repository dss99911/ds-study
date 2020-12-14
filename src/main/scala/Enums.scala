object Enums {

}

object EnumObj extends Enumeration
{
  type EnumObj = Value

  // Assigning values
  val first = Value("Thriller")
  val second = Value("Horror")
  val third = Value("Comedy")
  val fourth = Value("Romance")
}

sealed trait DayOfWeek
case object Sunday extends DayOfWeek
case object Monday extends DayOfWeek
case object Tuesday extends DayOfWeek
case object Wednesday extends DayOfWeek
case object Thursday extends DayOfWeek
case object Friday extends DayOfWeek
case object Saturday extends DayOfWeek