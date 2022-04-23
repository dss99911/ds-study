package spark

import org.apache.spark.storage.StorageLevel

/**
 * Spark also automatically persists some intermediate data in shuffle operations (e.g. reduceByKey)
 *
 * 다시쓰는 Dataframe의 경우, persist를 호출하는 것을 권장(셔플이 일어날 경우, 자동으로 persist되지만, 셔플이 안일어나면 저장이 안되므로)
 * unpersist() 는 안해줘도 자동으로 반환이 되는데, 빨리 반환하고 싶으면 호출하기
 * - !!!WARNING!!! Dataframe의 경우 물리적 실행계획 기반으로 캐싱이 된다고함.
 *      그래서, 원시 데이터를 읽으려고 했는데, 누군가 캐시를 해놓았다면, 캐싱된 데이터를 읽게되어 잘못 처리될 수 있다고 함.
 *      todo 그러면, 입력값이 다른 경우에도, 캐시로 인해, 결과 값이 달라질 수 있다는 이야기인듯. 그러면, 동시에 같은 애플리케이션을 실행안하도록 해야 하고, 사용 후에는 unpersist()를 해서, 다음에 동일 애플리케이션 호출 때, 캐시 값을 사용 못하게 해야 하는건가?
 *      pergist()는 지연 처리이므로, 캐싱된 데이터를 실제 실행하는 부분 이후에 unpersist()를 해야함.
 * https://spark.apache.org/docs/latest/rdd-programming-guide.html#rdd-persistence
 *
 * without `persist()` method, the data is not saved in memory
 * so, if you want to use the same data later, use `persist()`
 *
 * without `persist()`, if we call same DataSet multiple times, it runs multiple times as well
 *
 * 캐시를 사용하기 위해서, persist() 를 통해 리턴된 dataframe을 꼭 사용할 필요는 없다고함. persist()를 호출하는 dataframe을 사용해도됨.
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

  StorageLevel.MEMORY_ONLY // 메모리 공간을 벗어나면, 일부는 캐싱이 안되고, 필요할 때, 캐싱 안된 부분만 추가 처리함
  StorageLevel.MEMORY_AND_DISK // 메모리 공간을 벗어난 크기이면, 디스크에 저장
  StorageLevel.MEMORY_ONLY_SER // Serialize해서 메모리 공간을 절약 해줌, 하지만 Deserialize를 다시 해야 하기 때문에, 처리량은 늘어남

  spark.catalog.clearCache()
}
