# https://github.com/awslabs/aws-data-wrangler/tree/main/tutorials
# https://readthedocs.org/projects/aws-data-wrangler/downloads/pdf/latest/
import awswrangler as wr
import boto3
import pandas as pd

#%% exists
wr.s3.does_object_exist("s3://hyun.test/test.csv")

#%% list objects
wr.s3.list_objects("s3://hyun.test")


#%% change to custom seesion
#https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/002%20-%20Sessions.ipynb
import boto3
boto3.setup_default_session(region_name="us-east-2")


#%% fwf
import awswrangler as wr
import boto3

content = "1 Herfelingen27-12-18\n" \
          "2   Lambusart14-06-18\n" \
          "3Spormaggiore15-04-18"
boto3.client("s3").put_object(Body=content, Bucket="hyun.test", Key="fwf/file1.txt")

content = "4    Buizingen 05-09-19\n" \
          "5   San Rafael 04-09-19"
boto3.client("s3").put_object(Body=content, Bucket="hyun.test", Key="fwf/file2.txt")

path1 = f"s3://hyun.test/fwf/file1.txt"
path2 = f"s3://hyun.test/fwf/file2.txt"

df_fwf_widths = wr.s3.read_fwf([path1], names=["id", "name", "date"], widths=[1, 12, 8])
df_fwf = wr.s3.read_fwf([path2], names=["id", "name", "date"])

#%% delete object
wr.s3.delete_objects(path1)


#%%
# 직접 입력 받는 역할
import getpass
bucket = getpass.getpass()
local_file_dir = getpass.getpass()