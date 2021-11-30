#%% change to custom seesion, profile_name
#https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/002%20-%20Sessions.ipynb
# https://stackoverflow.com/questions/33378422/how-to-choose-an-aws-profile-when-using-boto3-to-connect-to-cloudfront
import boto3
boto3.setup_default_session(region_name="us-east-2", profile_name='name')