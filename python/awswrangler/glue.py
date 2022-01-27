import boto3
from pprint import pprint

glue_client = boto3.client('glue')

database_name = "hyun"
table_name = "some_table"

response = glue_client.get_table(
    DatabaseName=database_name,
    Name=table_name
)
original_table = response['Table']
#%%

allowed_keys = [
    "Name",
    "Description",
    "Owner",
    "LastAccessTime",
    "LastAnalyzedTime",
    "Retention",
    "StorageDescriptor",
    "PartitionKeys",
    "ViewOriginalText",
    "ViewExpandedText",
    "TableType",
    "Parameters"
]
updated_table = dict()
for key in allowed_keys:
    if key in original_table:
        updated_table[key] = original_table[key]

updated_table["StorageDescriptor"]['Columns'][0]['Comment'] = "this is id"
response = glue_client.update_table(
    DatabaseName=database_name,
    TableInput=updated_table
)

pprint(response)