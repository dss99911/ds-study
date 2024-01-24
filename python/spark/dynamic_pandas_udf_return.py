from functools import wraps

import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql.types import *
import pyspark.sql.functions as F

dtype_priority = [
    ('bool', BooleanType()),
    ('boolean', BooleanType()),
    ('datetime64[ns]', TimestampType()),
    ('Float64', DoubleType()),
    ('float64', DoubleType()),
    ('Int64', IntegerType()),
    ('int64', IntegerType()),
    ('object', StringType())
]
dtype_priority_index_map = {dtype[0]: index for index, dtype in enumerate(dtype_priority)}


def process_dynamic_pandas_udf_return(df: DataFrame, pandas_udf_func, cols=None, included_cols=None):
    """
    this function use checkpoint. need to set checkpoint dir
    :param pandas_udf_func:
        - parameter(col1: pd.Series, col2: pd.Series, ...)
        - return pd.DataFrame
    :param cols: parameter cols
    :param included_cols: the columns that you want to include in returned dataframe
    :return: DataFrame that include columns returned by pandas_udf_func
    """
    included_cols = make_list(included_cols)
    cols = make_list(cols)

    df_json_result = make_json_result(df, pandas_udf_func, cols, included_cols) \
        .checkpoint()

    feature_schema = find_feature_schema(df_json_result)
    return parse_json_result_to_features(df_json_result, feature_schema, included_cols)


def make_json_result(df, pandas_udf_func, cols, included_cols):
    func = pandas_udf_wrapper(pandas_udf_func)
    json_return_schema = "features string, dtypes string"
    return (
        df
        .withColumn("result", F.pandas_udf(func, json_return_schema)(*cols))
        .select(*included_cols, F.col("result.*"))
    )


def find_feature_schema(df_json_result):
    df = df_json_result.withColumn(
        "dtype_map",
        F.from_json(df_json_result["dtypes"], MapType(StringType(), StringType()))
    )

    dtype_per_col_name = (
        df
        .select(F.explode(df["dtype_map"]).alias("col_name", "dtype"))
        .distinct()
        .groupby("col_name")
        .agg(F.collect_set("dtype").alias("dtype"))
        .rdd.map(lambda x: x.asDict()).collect()
    )

    feature_schema = make_schema(dtype_per_col_name)
    return feature_schema


def parse_json_result_to_features(df_json_result, feature_schema: StructType, included_cols):
    features = (
        df_json_result
        .withColumn("feature_struct", F.from_json(df_json_result["features"], feature_schema))
        .select(*included_cols, "feature_struct.*")
        .checkpoint()
    )
    return rectify_features(features)


def rectify_features(features):
    features = rectify_timestamp(features)
    return features


def rectify_timestamp(features):
    def convert_col(col_name, dtype):
        if dtype == 'timestamp':  # on json, the value is saved with long in millis. so, need to convert to seconds
            return (F.unix_timestamp(col_name) / 1000).cast(TimestampType()).alias(col_name)
        else:
            return col_name

    return features.select(*[convert_col(col_name, dtype) for col_name, dtype in features.dtypes])


def convert_type(pandas_dtypes):
    priority_indexes = [dtype_priority_index_map[dtype] for dtype in pandas_dtypes]
    return dtype_priority[min(priority_indexes)][1]


def make_schema(dtype_per_col_name):
    return StructType(
        [
            StructField(r['col_name'], convert_type(r['dtype']))
            for r in dtype_per_col_name
        ]
    )


def convert_features_to_json(
        features: pd.DataFrame
) -> pd.DataFrame:
    features_json = features.apply(lambda x: x.to_json(), axis=1).rename("features")
    dtype_json = features.dtypes.apply(lambda x: str(x)).to_json()
    dtype_json = pd.Series([dtype_json] * len(features_json.index), index=features_json.index).rename("dtypes")
    result = pd.concat([features_json, dtype_json], axis=1)
    return result


def pandas_udf_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        features = f(*args, **kwds)
        return convert_features_to_json(features)

    return wrapper


def make_list(value):
    if value is None:
        return []

    if type(value) is not list:
        value = [value]
    return value