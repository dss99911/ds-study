object IfElse {
  if (1 == 1) {
    // A
  } else if (false) {
    // B
  } else {
    // C
  }

  val x = if (true) 1 else 2

  //switch case
  val result = 1 match {
    case 1 => "one"
    case 2 => "two"
    case _ => "not 1 or 2"
  }

  def getClassAsString(x: Any):String = x match {
    case s: String => s + " is a String"
    case i: Int => "Int"
    case f: Float => "Float"
    case l: List[_] => "List"
    case p: Person => "Person"
    case _ => "Unknown"
  }

  def isTrue(a: Any) = a match {
    case 0 | "" => false
    case _ => true
  }

  10 match {
    case 1 => println("one, a lonely number")
    case x if x == 2 || x == 3 => println("two's company, three's a crowd")
    case x if (x > 3) =>
      println("4+, that's a party")
    case _ => {
      println("i'm guessing your number is zero or less")
    }
  }

  while(true) {
  }

  // do-while
  do {
  }
  while(true)
}

