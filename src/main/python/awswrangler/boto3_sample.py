import logging
import boto3
from botocore.exceptions import ClientError
import os


#%%
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    s3_client = boto3.client('s3')
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
#%%

def exists(bucket, path):
    s3_client = boto3.client('s3')
    try:
        s3_client.head_object(Bucket=bucket, Key=path)
        return True
    except ClientError as ex:
        if ex.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            return False
        raise ex

exist = exists("hyun.test", "test.csv")

#%% download
s3_client = boto3.client('s3')
s3_client.download_file("hyun.test", "object", "path")

#%% delete dir
s3 = boto3.resource('s3')
bucket = s3.Bucket('mybucket')
bucket.objects.filter(Prefix="myprefix/").delete()

#%%