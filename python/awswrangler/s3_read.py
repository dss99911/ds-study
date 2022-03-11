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

def get_objects(s3_prefix, file_postfix=""):
    list_dpd = wr.s3.list_objects(s3_prefix)
    return [f for f in list_dpd if f.endswith(file_postfix)]


def download_file(s3_path, local_path):
    wr.s3.download(path=s3_path, local_file=local_path)
    return local_path


def download_files(s3_path, local_path, file_postfix=""):
    import os
    os.mkdir(local_path)
    for o in get_objects(s3_path, file_postfix):
        print(o, s3_path, o.split(s3_path)[1])
        download_file(o, local_path + o.split(s3_path)[1])

download_files("s3://some_dir", "some_local_dir", ".parquet")

