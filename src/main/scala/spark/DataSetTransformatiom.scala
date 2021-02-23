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


  val wordCunt = text.flatMap(line => line.split(" "))
    .groupByKey(s => identity(s)).count()

  //groupby한 후에, group별로 reduce로 하나로 합친다
  val wordCount2 = text.flatMap(line => line.split(" "))
    .map((_, 1))
    .groupByKey(_._1)
    .reduceGroups((a, b) => (a._1, a._2 + b._2))
    .count()

  wordCount.collect()//make Dataset to array

  /**
   * without `persist()` method, the data is not saved in memory
   * so, if you want to use the same data later, use `persist()`
   *
   * without `persist()`, if we call same DataSet multiple times, it runs multiple times as well
   */
  def persist() = {
    val uppercaseText = text.map(t => t.toUpperCase())
    uppercaseText.persist()
    uppercaseText.cache()//cache() is same with persist(). but cache() is only in memory. but persist(level) can set where to save.

    // persist data set is automatically cleared. but it takes time(least-recently-used (LRU) fashion)
    // so, If you want to clear directly after it's finished to use. then call 'unpersist()\'
    uppercaseText.unpersist()
  }
}
