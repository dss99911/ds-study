from pyspark.sql.dataframe import DataFrame
from util.util import *

def array_functions(df: DataFrame):
    df.groupBy("sequence") \
        .agg(collect_set("item").alias("list")) \
        .withColumn("list", array_union(col("list"), array(lit("d")))) \
        .withColumn("size", size(col("list")))