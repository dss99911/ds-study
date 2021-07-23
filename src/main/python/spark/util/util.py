import sys

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from slackclient import SlackClient
from pyspark.sql import functions as F, SparkSession
from pyspark.sql.types import *
from pyspark.sql import DataFrame
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
import res.resource_dev as res_dev
import res.resource_live as res_live

def res():
    return res_live if(sys.argv[1] == "live") else res_dev

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
    df = df.withColumn("seq", F.row_number().over(window))
    df = df.filter(F.col("seq") == 1)
    df = df.drop("seq")
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
