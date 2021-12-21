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

#%% read

df_read = wr.s3.read_csv([path1, path2])
df_read_by_dir = wr.s3.read_csv(dir_csv)
df_read_parse_dates = wr.s3.read_csv(dir_csv, parse_dates=["dt", "obs_time"])
# df_read_json = wr.s3.read_json([path1, path2])
# df_read_json = wr.s3.read_parquet(path1, dataset=True)
# df_read_excel = wr.s3.read_excel([path1, path2])


#%% download
import os
import getpass
local_file_dir = getpass.getpass()
path1 = f"{dir_csv}/file1.csv"
local_file = os.path.join(local_file_dir, "file1.csv")
wr.s3.download(path=path1, local_file=local_file)

pd.read_csv(local_file)

