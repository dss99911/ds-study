from spark.read import *

data = [["1", "2020-02-01"], ["2", "2019-03-01"], ["3", "2021-03-01"]]

df = spark.createDataFrame(data, ["id", "input"])

df = df.withColumn("aa", current_date()) # date type
df = df.withColumn("ab", date_add(col("aa"), 5)) # date type
df = df.withColumn("ac", col("aa").cast(TimestampType()).cast("double") - col("ab").cast(TimestampType()).cast("double"))
df.show()
