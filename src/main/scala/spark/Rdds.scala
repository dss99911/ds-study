package spark

import org.apache.spark.{HashPartitioner, Partitioner}
import org.apache.spark.sql.Row
import spark.Read.Person

/**
 * 사용하는 가장 큰 이유
 * - 사용자 정의 파티셔닝 : 데이터 치우침(skew) 같은 문제를 피하고, 셔플을 피하기
 */
class Rdds {
  val df = Read.getListDataFrame()

  /**
   * able to use system command
   */
  def pipe() = {
    df.rdd.pipe("wc -l")
  }

  //make PairRDD : 키 별로, partition을 만드는 듯
  df.rdd.keyBy(r => r.getString(0))
    .mapValues(r => r.getInt(1))

    .lookup("a") // find values whose key is 'a'

  /**
   * initial value for each partitions
   * param1 : accumulate on each partition
   * param2 : aggregate between accumulted value of each partition.
   *
   */
  def aggregates() = {
    val inputRDD = df.rdd.map(r => ("a", 1))
    //aggregate
    def param1= (accu:Int, v:(String,Int)) => accu + v._2
    def param2= (accu1:Int,accu2:Int) => accu1 + accu2

    //aggregate's parame2 is processed on driver node. so, if param2's values are too big. then there can be out of memory
    val result2 = inputRDD.aggregate(0)(param1,param2)

    //if key exists, able to use treeAggregate. these is processed on worker nodes by tree way
    // param2 is handled on each worker node. depth shows how many worker nodes are combined by tree way together.
    df.rdd.keyBy(r => r.getInt(0))
      .treeAggregate(0)((i: Int, tuple: (Int, Row)) => i, (i: Int, i1: Int) => i + i1, 3)

    //키를 기준으로 aggregate 함.
//    inputRDD.aggregateByKey()//initialValue가 람다가 아닌 값.
//    inputRDD.combineByKey()//initialValue를 생성하는 람다 사용. 파티션 갯수 설정 가능
//    inputRDD.foldByKey()//파티션끼리의 combine이 없음.

    //각 키별 A, B RDD의 값을 그룹핑함
    val tuples: Array[(String, (Iterable[Int], Iterable[Int]))] = inputRDD.cogroup(inputRDD).collect()
    //파티션별로 Iterator를 만들어서, coalescece(1)을 만듬
    df.rdd.glom()
  }


  //파티션의 index를 제공하여, 해당 iterator가 어느 partition에 있는자 알 수 있다.
  // mapPartition시 파티션 분할이 잘 됐는지 디버깅할 때 사용.
  df.rdd.mapPartitionsWithIndex((i: Int, rows: Iterator[Row]) => Seq(s"parition number : $i, rows $rows").toIterator)


  //사용자 정의 파티셔닝
  df.rdd.keyBy(_.getInt(0)).partitionBy(new HashPartitioner(10))
  class CustomPartitioner extends Partitioner {
    override def numPartitions: Int = 3
    override def getPartition(key: Any): Int = 0 //0부터 2까지의 파티션 index를 리턴 해야 하는듯.
  }
  df.rdd.keyBy(_.getInt(0)).partitionBy(new CustomPartitioner())

  //kryo
  SparkSessions.createSparkSession().sparkContext.getConf.registerKryoClasses(Array(classOf[Person]))
}
