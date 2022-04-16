package spark

import org.apache.spark.sql.SparkSession

class Gpu {
  def explainGpu(spark: SparkSession) = {
    import spark.implicits._

    val data = 1 to 10000

    val df1 = data.toSeq.toDF()
    val df2 = data.toSeq.toDF()
    val out = df1.as("df1").join(df2.as("df2"), $"df1.value" === $"df2.value")
    out.count()
    out.explain()

  }
}
