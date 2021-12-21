#%% write pandas df to s3
import awswrangler as wr
import boto3
import pandas as pd

df1 = pd.DataFrame({
    "id": [1, 2],
    "name": ["foo", "boo"]
})

df2 = pd.DataFrame({
    "id": [3],
    "name": ["bar"]
})

dir_csv = "s3://hyun.test/csv"
path1 = f"{dir_csv}/test1.csv"
path2 = f"{dir_csv}/test2.csv"

#%% write text
script = """
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("docker-awswrangler").getOrCreate()
sc = spark.sparkContext

print("Spark Initialized")
"""

_ = boto3.client("s3").put_object(
    Body=script,
    Bucket="hyun.test",
    Key="test.py"
)

#%% write dataframe
wr.s3.to_csv(df1, path1, index=False)
wr.s3.to_csv(df1, path2, index=False)
wr.s3.to_json(df1, path1, index=False)
wr.s3.to_parquet(df1, path1, dataset=True, mode="overwrite", partition_cols=["date"])
wr.s3.to_parquet(df1, path1, dataset=True, mode="append")
wr.s3.to_parquet(df1, path1, dataset=True, mode="overwrite_partitions", partition_cols=["date"])

#%% upload
import os
import getpass
local_file_dir = getpass.getpass()

local_file = os.path.join(local_file_dir, "file1.csv")
wr.s3.upload(local_file=local_file, path=path1)