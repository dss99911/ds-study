package spark

object Files {
  val spark = SparkSessions.createSparkSession()

  import org.apache.hadoop.fs.{FileSystem, FileUtil, Path}

  def copyFile(sourcePath: String, destinationPath: String) = {
    val srcPath = new Path(sourcePath)
    val srcFs = FileSystem.get(srcPath.toUri(), spark.sparkContext.hadoopConfiguration)
    val dstPath = new Path(destinationPath)
    val dstFs = FileSystem.get(dstPath.toUri(), spark.sparkContext.hadoopConfiguration)
    dstFs.delete(dstPath, true)
    FileUtil.copy(srcFs, srcPath, dstFs, dstPath, false, false, spark.sparkContext.hadoopConfiguration)
  }

  def copySingleFileOfPartitionToOutside(sourcePath: String, partitionName: String, destinationDir: String, filePostfix: String) = {
    val taskPath = new Path(sourcePath)
    val fs = FileSystem.get(taskPath.toUri(), spark.sparkContext.hadoopConfiguration)
    val status = fs.listStatus(taskPath)
    status.filter(p => p.getPath.toString.startsWith(s"$sourcePath/$partitionName"))
      .flatMap(p => fs.listStatus(p.getPath))
      .foreach(x=> {
        val sourcePath = x.getPath.toString
        val name = sourcePath.split("\\/")
          .filter(p => p.startsWith(s"$partitionName="))
          .head.split("=").last
        val destinationPath = destinationDir + "/" + name + filePostfix
        copyFile(sourcePath, destinationPath)
      })
  }

}
