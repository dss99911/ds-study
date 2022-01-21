import json
import numpy as np
import pandas as pd
import boto3
from pandas import json_normalize
from boto3.dynamodb.conditions import Key
#%%

key_name = "key_name"
key_value = "key_value"
table = "table"
projection = "a, b, c"

#%% write
# https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/028%20-%20DynamoDB.ipynb
import awswrangler as wr
import pandas as pd
wr.dynamodb.put_df(
    df=pd.DataFrame({'key': [1, 2, 3]}),
    table_name='table'
)


#%% read paging
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table)
query_params = {"KeyConditionExpression": Key(key_name).eq(key_value),
                "ProjectionExpression": projection}
response = table.query(**query_params)
trx = json_normalize(response["Items"])
while 'LastEvaluatedKey' in response.keys():
    query_start_key = response['LastEvaluatedKey']
    query_params = {
        "KeyConditionExpression": Key(key_name).eq(key_value),
        "ExclusiveStartKey": query_start_key
    }
    response = table.query(**query_params)
    temp_trx = json_normalize(response["Items"])
    trx = pd.concat([trx, temp_trx], axis=0)
