import sys
from pyspark.ml.functions import *

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
from slackclient import SlackClient

import spark.res.resource_dev as res_dev
import spark.res.resource_live as res_live


def res():
    return res_live if(sys.argv[1] == "live") else res_dev


def get_argv(index):
    index = index+2 # 0 is for file, 1 is for dev or live
    return sys.argv[index] if(index < len(sys.argv)) else None


def create_spark_session(name, use_delta=True):
    builder = SparkSession.builder \
        .appName(name) \
        .enableHiveSupport() \
        .config("spark.sql.hive.manageFilesourcePartitions", False)

    if use_delta:
        builder = builder.config("spark.jars.packages", "io.delta:delta-core_2.12:0.8.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    return builder.getOrCreate()


def window_filter(df: DataFrame, window):
    df = df.withColumn("seq", row_number().over(window))
    df = df.filter(col("seq") == 1)
    df = df.drop("seq")
    return df

def rename_agg(df):
    for c in df.columns:
        if "(" not in c :
            continue
        new_col = c.replace("(", "_")
        new_col = new_col.replace(")", "")
        df = df.withColumnRenamed(c, new_col)
    return df

def send_slack_message(text, channel="@hyun", username="", icon_emoji=""):
    slack = SlackClient('oauth-token')

    if isinstance(text, DataFrame):
        text = text._jdf.showString(20, int(False), False)

    slack.api_call(
        'chat.postMessage',
        channel=channel,
        text=text,
        username=username,
        icon_emoji=icon_emoji
    )


def show_hist(df, value_col, digit_count=2):
    res = df.withColumn("key", format_number(percent_rank().over(Window.orderBy(value_col)), digit_count)) \
        .groupBy("key").agg(mean(value_col).alias(value_col)) \
        .select("key", value_col) \
        .sort("key")
    z.show(res)
