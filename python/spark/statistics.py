from datetime import datetime, date
from spark.util.util import *

spark = SparkSession.builder.getOrCreate()

spark_df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])
spark_df.summary().show()

#+-------+------------------+------------------+-------+
#|summary|                 a|                 b|      c|
#+-------+------------------+------------------+-------+
#|  count|                 3|                 3|      3|
#|   mean|2.3333333333333335|3.3333333333333335|   null|
#| stddev|1.5275252316519468|1.5275252316519468|   null|
#|    min|                 1|               2.0|string1|
#|    25%|                 1|               2.0|   null|
#|    50%|                 2|               3.0|   null|
#|    75%|                 4|               5.0|   null|
#|    max|                 4|               5.0|string3|
#+-------+------------------+------------------+-------+


# get_dummies
def get_dummies(df: DataFrame, columns):
    for c in columns:
        category = df.select(c).distinct().rdd.flatMap(lambda x: x).collect()
        for cat in category:
            df = df.withColumn(f"{c}_{cat}", when(col(c) == cat, 1).otherwise(0))
        df = df.drop(c)

    return df


get_dummies(spark_df, ['b', 'c']).show()