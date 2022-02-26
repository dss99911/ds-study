import sys
from pyspark.ml.functions import *

from pyspark.sql import DataFrame, Row
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
from slackclient import SlackClient
import builtins as B

import spark.res.resource_dev as res_dev
import spark.res.resource_live as res_live


def res():
    return res_live if(sys.argv[1] == "live") else res_dev


def get_argv(index):
    index = index+2 # 0 is for file, 1 is for dev or live
    return sys.argv[index] if(index < len(sys.argv)) else None


def create_spark_session(name, use_delta=False):
    builder = SparkSession.builder \
        .appName(name) \
        .enableHiveSupport()

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


def rename_columns_by_name(df: DataFrame, func_new_col, exclude=[]):
    for c in df.columns:
        if c in exclude:
            continue
        df = df.withColumnRenamed(c, func_new_col(c))
    return df


def rename_columns_by_list(df: DataFrame, new_cols: list):
    for i, c in enumerate(df.columns):
        df = df.withColumnRenamed(c, new_cols[i])
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


def agg_by_dict(agg_df, agg_dict, rename_column=False, prefix=None, postfix=None) -> DataFrame:
    """
    percentile_approx(val, 0.5) is not supported
    """
    agg_list = []

    def make_expr(f, c):
        if type(f) == str:
            f_name = f
            e = expr(f"{f}({c})")
        else:
            f_name = f.__name__
            e = f(c)

        if rename_column:
            col_name = "_".join(list(B.filter(lambda n: n is not None, [prefix, c, f_name, postfix])))
            e = e.alias(col_name)
        return e

    for k in agg_dict:
        if type(agg_dict[k]) == list:
            for f in agg_dict[k]:
                agg_list.append(make_expr(f, k))
        else:
            agg_list.append(make_expr(agg_dict[k], k))

    return agg_df.agg(*agg_list)


def get_cols(df, exclude_cols, types):
    return list(B.filter(lambda c: c.name not in exclude_cols and c.dataType in types, df.schema.fields))


def get_numeric_cols(df, exclude_cols):
    return get_cols(df, exclude_cols, [LongType(), DoubleType(), IntegerType(), FloatType(), DecimalType(), ShortType(), ByteType()])