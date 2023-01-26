package com.balancehero.acs.utils

import com.typesafe.config.{Config, ConfigFactory}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.SparkSession.Builder

trait SparkRunner extends Serializable {
  val appName: String = getClass.getSimpleName.split('$').head

  def setConf(builder: Builder)

  private val builder: Builder = SparkSession.builder.appName(appName)
  setConf(builder)

  lazy val spark: SparkSession = builder.enableHiveSupport().getOrCreate()

  lazy val conf: Config = ConfigFactory.load
  
}