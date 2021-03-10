object Strings {
  val firstName = "dd"
  val lastName = "dd"
  val number = 123.123123
  //used s"" for types
  println(s"$firstName $lastName ${1+1}")
  println(f"$number%1.2f %%")//for printing %, use %%

  val speech = """Four score and
               seven years ago
               our fathers ..."""

  //use margin
  val speech2: String = """Four score and
                 |seven years ago
                 |our fathers ...""".stripMargin

  //split and join strings.
  "a,b,c".split(",")
    .map(x => s"lower(sms_sender) rlike lower('$x')")
    .mkString(" or ")
}
