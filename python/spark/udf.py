# %%
from pyspark.sql.functions import udf
from pyspark.sql.functions import col, asc, desc
from pyspark.sql.types import FloatType, StructType, StringType, StructField, DoubleType

from spark.DataFrameRead import create_by_row

x2 = udf(lambda x: x * 2, StringType())
create_by_row().withColumn("x2", x2("x"))  # make x2 column from x column

# %%


# https://docs.databricks.com/spark/latest/spark-sql/udf-python.html


from difflib import SequenceMatcher

from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType, StructType, StringType, StructField
from pyspark.sql.functions import udf
import pyspark.sql.functions as F


def getSentenceDiffRatio(stc1, stc2):
    # ratio = SequenceMatcher(lambda x: x == " ", stc1.split(), stc2.split())
    result = None
    try:
        if (stc1 != None) & (stc2 != None):
            ratio = SequenceMatcher(lambda x: x == " ", stc1.split(), stc2.split()).ratio()

            result = { \
                "ratio": ratio, \
                "status": 'SUCCESS', \
                "sentence1": stc1, \
                "sentence2": stc2, \
                "errorMessage": None}
        else:
            result = { \
                "ratio": None, \
                "status": 'FAILURE', \
                "sentence1": stc1, \
                "sentence2": stc2, \
                "errorMessage": None}

    except Exception as error:
        result = { \
            "ratio": None, \
            "status": 'FAIL', \
            "sentence1": stc1, \
            "sentence2": stc2, \
            "errorMessage": error.getMessage()}

    finally:
        return result


diffRatioSchema = StructType([ \
    StructField('ratio', FloatType(), False) \
    , StructField('status', StringType(), False) \
    , StructField('sentence1', StringType(), False) \
    , StructField('sentence2', StringType(), False) \
    , StructField('errorMessage', StringType(), True) \
    ])

getSentenceDiffRatioUDF = udf(lambda x, y: getSentenceDiffRatio(x, y), diffRatioSchema)

spark = SparkSession.builder.appName("acs_tx_extractor").getOrCreate()
spark.udf.register('getSentenceDiffRatioUDF', getSentenceDiffRatio, diffRatioSchema)

#%% pandas udf : pandas의 기능을 쓰고 싶을 때 쓰는듯.
from pyspark.sql.functions import pandas_udf
import pandas as pd
import numpy as np

def func(pdf: pd.DataFrame) -> pd.Series:
    out = pdf.apply(lambda x: np.dot(x["target_vector"].toArray(), x["right_vector"].toArray()), axis=1)
    return out

my_udf = pandas_udf(func, returnType=DoubleType())

out = spark.read.parquet("some")\
    .select(my_udf("two_vectors").alias("cosine_similarity"))