import argparse

from pyspark.sql import SparkSession

# todo modify path properly.
# from util.common import *
from common import *


def get_spark(configs={}) -> SparkSession:
    builder = SparkSession.builder.appName("spark-app") \
        .enableHiveSupport() \
        .config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory") \
        .config("spark.sql.broadcastTimeout", 3000000)

    for key, value in configs.items():
        builder = builder.config(key, value)

    return builder.getOrCreate()
