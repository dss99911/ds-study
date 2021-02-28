package spark

/**
 * Spark also automatically persists some intermediate data in shuffle operations (e.g. reduceByKey)
 *
 * 다시쓰는 Dataframe의 경우, persist를 호출하는 것을 권장(셔플이 일어날 경우, 자동으로 persist되지만, 셔플이 안일어나면 저장이 안되므로)
 * unpersist() 는 안해줘도 자동으로 반환이 되는데, 빨리 반환하고 싶으면 호출하기
 * https://spark.apache.org/docs/latest/rdd-programming-guide.html#rdd-persistence
 *
 * without `persist()` method, the data is not saved in memory
 * so, if you want to use the same data later, use `persist()`
 *
 * without `persist()`, if we call same DataSet multiple times, it runs multiple times as well
 */
class Persist {
  val (spark, text) = Read.getTextDataSet()
  import spark.implicits._

  val uppercaseText = text.map(t => t.toUpperCase())
  uppercaseText.persist()
  uppercaseText.cache()//cache() is same with persist(). but cache() is only in memory. but persist(level) can set where to save.

  // persist data set is automatically cleared. but it takes time(least-recently-used (LRU) fashion)
  // so, If you want to clear directly after it's finished to use. then call 'unpersist()\'
  uppercaseText.unpersist()
}
