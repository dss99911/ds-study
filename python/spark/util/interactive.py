from spark.util.util import *
# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt

try:
    #intellij doesn't recognize spark instance on jupyter notebook.
    #this will occur error. but, intellij will recognize spark variable
    # noinspection PyUnresolvedReferences,PyUnboundLocalVariable
    spark: SparkSession = spark
except:
    pass

spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
sc = spark.sparkContext