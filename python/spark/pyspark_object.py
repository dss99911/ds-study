df = spark.read.parquet("json.parqeut").select("json")
json_schema = spark.read.json(df.rdd.map(lambda row: row.json)).schema
df.withColumn("struct", F.from_json("json", json_schema)).select("struct.*").write.parquet("struct.parquet", mode="overwrite")