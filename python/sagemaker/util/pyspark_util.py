import argparse

from pyspark.sql import SparkSession
from util.common import *


def get_args(name, arg_type=str, default=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--" + name, type=arg_type, default=default)
    args, _ = parser.parse_known_args()
    return getattr(args, name)


def get_args_schema():
    return get_args("schema", default="stage")


def get_args_schema_path():
    return get_args("schema_path", default="s3://hyun/stage")


def get_spark() -> SparkSession:
    return (
        SparkSession.builder.appName("spark-app")
        .config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")
        .config("spark.sql.broadcastTimeout", 3000000)
        .enableHiveSupport()
        .getOrCreate()
    )