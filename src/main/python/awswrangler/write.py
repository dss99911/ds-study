#%% write pandas df to s3
import awswrangler as wr
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

#%% write
wr.s3.to_csv(df1, path1, index=False)
wr.s3.to_csv(df1, path2, index=False)
# wr.s3.to_json(df1, path1, index=False)
# wr.s3.to_parquet(df1, path1, index=False)
# wr.s3.to_excel(df1, path1, index=False)

#%% upload
import os
import getpass
local_file_dir = getpass.getpass()

local_file = os.path.join(local_file_dir, "file1.csv")
wr.s3.upload(local_file=local_file, path=path1)