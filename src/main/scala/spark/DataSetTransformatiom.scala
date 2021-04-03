package spark


/**
 * - DataSet 은 성능상좋지 않다. 가능하면 DataFrame을 쓰고,
 * - class구조 형태로의 가공처리를 많이 해야 할 경우에만 쓰기.
 * - 처리 파이프라인의 처음과 끝 작업에서 주로 사용
 */
class DataSetTransformatiom {
  val (spark, text) = Read.getTextDataSet()
  import spark.implicits._
  text.first()
  text.count()
  text.filter((str: String) => str.contains("aa"))
  text.map(line => line.split(" ").size)
    .reduce((a, b) => Math.max(a, b))

  text.joinWith(text, text.col("a") === text.col("a"))
    .map((tuple: (String, String)) => tuple)//join을 해도 타입이 유지됨.
    .selectExpr("_1.a")//타입의 특정 필드를 이런식으로 select도 가능


  val wordCount = text.flatMap(line => line.split(" "))
    .groupByKey(s => identity(s)).count()

  //groupby한 후에, group별로 reduce로 하나로 합친다
  val wordCount2 = text.flatMap(line => line.split(" "))
    .map((_, 1))
    .groupByKey(_._1)
    .reduceGroups((a, b) => (a._1, a._2 + b._2))
    .count()

  wordCount.collect()//make Dataset to array

  //make dataset to DataFrame. need `import spark.implicits._`
  //If use kryo, then, field is not changed to column. but it's changed to binary.
  wordCount.toDF()

}
