package spark

class Accumulator {
  val spark = SparkSessionCreate.createSparkSession()
  val sc = spark.sparkContext
  val accum = sc.longAccumulator("My Accumulator")
  sc.parallelize(Array(1, 2, 3, 4)).foreach(x => accum.add(x))

  accum.value
}
