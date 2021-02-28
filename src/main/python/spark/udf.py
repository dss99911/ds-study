# https://docs.databricks.com/spark/latest/spark-sql/udf-python.html

from difflib import SequenceMatcher

from org.apache.spark.sql import SparkSession
from pyspark.sql.types import FloatType, StructType, StringType, StructField
from pyspark.sql.functions import udf
import pyspark.sql.functions as F

def getSentenceDiffRatio(stc1, stc2):
    # ratio = SequenceMatcher(lambda x: x == " ", stc1.split(), stc2.split())
    result = None
    try:
        if (stc1 != None) & (stc2 != None ) :
            ratio = SequenceMatcher(lambda x: x == " ", stc1.split(), stc2.split()).ratio()

            result = { \
                "ratio": ratio, \
                "status": 'SUCCESS', \
                "sentence1": stc1, \
                "sentence2": stc2, \
                "errorMessage": None }
        else:
            result = { \
                "ratio": None, \
                "status": 'FAILURE', \
                "sentence1": stc1, \
                "sentence2":stc2, \
                "errorMessage": None }

    except Exception as error:
        result = { \
            "ratio": None, \
            "status": 'FAIL', \
            "sentence1": stc1, \
            "sentence2":stc2, \
            "errorMessage": error.getMessage() }

    finally:
        return result


diffRatioSchema = StructType([ \
    StructField('ratio', FloatType(), False) \
    , StructField('status', StringType(), False) \
    , StructField('sentence1', StringType(), False) \
    , StructField('sentence2', StringType(), False) \
    , StructField('errorMessage', StringType(), True) \
    ])


getSentenceDiffRatioUDF = udf(lambda x,y: getSentenceDiffRatio(x,y), diffRatioSchema)

spark = SparkSession.builder.appName("acs_tx_extractor").getOrCreate()
spark.udf.register('getSentenceDiffRatioUDF',getSentenceDiffRatio,diffRatioSchema)