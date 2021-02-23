package spark

import org.apache.spark.sql.SparkSession
import spark.Read.spark

import java.net.InetAddress
import java.util.concurrent.Executors
import scala.concurrent.ExecutionContext

object Cluster {

  def getCpuCount() = {
    //https://kb.databricks.com/clusters/calculate-number-of-cores.html
    val spark: SparkSession = SparkSessions.createSparkSession()
    val clusterCount = spark.sparkContext.statusTracker.getExecutorInfos.length //cluster count including driver node
    val coreCount = java.lang.Runtime.getRuntime.availableProcessors //
    clusterCount * coreCount
  }


  /**
   * as each node's ip address is different.
   * check with ip address
   */
  def findCurrentCluster() = {
    import spark.implicits._

    val ip = InetAddress.getLocalHost()
    println(s"Driver program's ip address : $ip")

    (0 to 100).toSeq
      .toDS()
      .repartition(50)//만약 한 worker node에서만 호출되게 하고 싶으면, repartition(1)해야 함
      .map(num => InetAddress.getLocalHost() + "")
      .filter(s => {Thread.sleep(10000); true})
      .distinct()
      .show(100, truncate = false)

  }

  /**
   * This is not recommended. able to handle multiple job on each worker node
   */
  def processMultipleJob(args: Array[String]): Unit = {
    val spark = SparkSession.builder.appName("acs_message_analyzer")
      //      .config("spark.scheduler.mode", "FAIR")
      .enableHiveSupport().getOrCreate()
    import spark.implicits._

    import java.net.InetAddress
    import java.util.concurrent.TimeUnit
    import scala.concurrent.{Await, Future}
    import scala.concurrent.ExecutionContext.Implicits.global
    import scala.concurrent.duration.Duration
    import scala.util.{Failure, Success}

    val service = Executors.newFixedThreadPool(9)
    val context = ExecutionContext.fromExecutor(service)
    Seq(2,3,4,2,3,4,2,3,4)
      .zipWithIndex.map { case (e, i) =>
      Future[Int] {
        println("[AA]start" + i)
        val strings = spark.read.parquet(s"s3://hyun" + e)
          .repartition(1)
          .map(a => InetAddress.getLocalHost().toString)
          .filter { a=>
            Thread.sleep(10)
            true
          }
          .distinct()
          .collect()
        println("[AA]finish" + i + " : " + strings.mkString(","))
        i


      }(context)
    }.foreach { f =>
      val start = System.currentTimeMillis()
      println("[AA]wait " + start)
      println("[AA]wait finish " + Await.result(f, Duration(100, TimeUnit.SECONDS)) + ", " + (System.currentTimeMillis() - start))
    }

    service.shutdown()
  }
}
