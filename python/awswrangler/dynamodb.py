# https://github.com/aws/aws-sdk-pandas/blob/main/tutorials/028%20-%20DynamoDB.ipynb
import decimal
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


#%% create table
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
client = boto3.client('dynamodb')
table_name = "some_table"
response = client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
    ],
    BillingMode='PAY_PER_REQUEST',
    TableClass='STANDARD'
)


#%% table description
table_name = 'table_name'
client = boto3.client('dynamodb')
client.describe_table(
    TableName=table_name
)


#%% write
# https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/028%20-%20DynamoDB.ipynb
import awswrangler as wr
import pandas as pd
wr.dynamodb.put_df(
    df=pd.DataFrame({'key': [1, 2, 3]}),
    table_name='table'
)
#%% scan limited rows. if the attribute is null. it's not included
single_row = client.scan(TableName=table_name, Limit=1)
types = set([list(v.keys())[0] for v in single_row['Items'][0].values()])

#%%
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
query_params = {
    "KeyConditionExpression": Key('androidId').eq("9183f950d87c0f2c")
}
response = table.query(**query_params)

#%% get attritubes and type

from collections import defaultdict
import decimal

type_dict = {
    "NULL": None,
    "S": "string",
    "N": "double",
    "B": "binary",
    "BOOL": "boolean",
    "L": "array",
    "NS": "array",
    "SS": "array",
    "BS": "array",
    decimal.Decimal: "double",
    str: "string"
}


def _get_type(value):
    if type(value) is dict and len(value) == 1:
        t, v = list(value.items())[0]
        value_type = type_dict.get(t)
        if value_type is None:
            raise ValueError(t, "on dict is not recognized")
        return value_type

    value_type = type_dict.get(type(value))

    if value_type is None:
        raise ValueError(type(value), "is not recognized")
    return value_type


def get_dynamodb_table_schema(table_name, limit=1000):
    client = boto3.client('dynamodb', "ap-south-1")
    response = client.scan(TableName=table_name, Limit=limit)
    col_types = defaultdict(set)
    for item in response['Items']:
        for col, value in item.items():
            col_types[col].add(_get_type(value))

    def choose_type(type_set):
        types = [t for t in type_set if t is not None]
        return types[0] if types else None

    return {k: choose_type(v) for k, v in col_types.items()}


def create_table_from_dynamodb(hive_table_name, dynamodb_table_name, limit=1000,
                               default_type="string", schema_overrides={}):
    schema = get_dynamodb_table_schema(dynamodb_table_name, limit)
    schema.update(schema_overrides)

    for k, v in schema.items():
        if v is None:
            schema[k] = default_type

    create_statement = f"""
    CREATE EXTERNAL TABLE {hive_table_name} 
    ({", ".join([f"{col} {type}" for col, type in schema.items()])})
    STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler' 
    TBLPROPERTIES ("dynamodb.table.name" = "{dynamodb_table_name}", 
    "dynamodb.column.mapping" = "{",".join([f"{col}:{col}" for col in schema.keys()])}");
    """
    return create_statement
    # Spark 에서 안되고, hive에서 sql문을 호출하면, 테이블 생성됨.
    # spark.sql(create_statement)


print(create_table_from_dynamodb("hyun2.dev_sms_message_pattern3", "dev-sms-message-pattern"))


#%% scan all rows
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

response = table.scan()
items = response['Items']
while 'LastEvaluatedKey' in response:
    print(response['LastEvaluatedKey'])
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    items.extend(response['Items'])


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
