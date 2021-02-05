package spark

import org.apache.spark.sql.SparkSession
import spark.Read.spark

import java.net.InetAddress

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
}
