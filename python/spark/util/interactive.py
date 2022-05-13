from spark.util.util import *
# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt

try:
    #intellij doesn't recognize spark instance on jupyter notebook.
    #this will occur error. but, intellij will recognize spark variable
    # noinspection PyUnresolvedReferences,PyUnboundLocalVariable
    import __main__
    spark: SparkSession = __main__.global_dict["spark"]  # for livy session
    spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
    sc = spark.sparkContext
except:
    pass