
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
spark.sparkContext._conf.getAll()

# pyspark shell에서 conf 설정하기
conf = spark.sparkContext._conf.setAll([('spark.plugins', 'com.nvidia.spark.SQLPlugin'), ('spark.rapids.memory.gpu.pooling.enabled', 'false')])

spark.sparkContext.stop()

spark = SparkSession.builder.config(conf=conf).getOrCreate()
