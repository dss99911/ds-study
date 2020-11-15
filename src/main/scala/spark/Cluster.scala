package spark

import org.apache.spark.sql.SparkSession

object Cluster {

  def getCpuCount() = {
    //https://kb.databricks.com/clusters/calculate-number-of-cores.html
    val spark: SparkSession = SparkSessions.createSparkSession()
    val clusterCount = spark.sparkContext.statusTracker.getExecutorInfos.length //cluster count including driver node
    val coreCount = java.lang.Runtime.getRuntime.availableProcessors //
    clusterCount * coreCount
  }

}
