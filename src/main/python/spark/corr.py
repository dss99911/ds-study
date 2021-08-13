from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import ChiSquareTest
from pyspark.ml.stat import Correlation
from pyspark.ml.functions import *
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import *


def get_numeric_corr(df: DataFrame, col_label: str, cols_feature):
    corrs = list(map(lambda c: corr(col_label, c).alias(f"{c}_corr"),cols_feature))
    return df.select(*corrs)

def get_categorical_corr(df: DataFrame, col_label: str, cols_feature):
    """
    작을 수록 좋음
    """
    indexer = StringIndexer(inputCols=cols_feature, outputCols=[f"{c}_indexed" for c in cols_feature])
    assembler = VectorAssembler(inputCols=[c + "_indexed" for c in cols_feature], outputCol="category_features")
    pipeline = Pipeline(stages=[indexer, assembler])
    pipe = pipeline.fit(df)
    data = pipe.transform(df)

    pearson_chi_test_result = ChiSquareTest.test(data, "category_features", col_label)

    return pearson_chi_test_result \
        .withColumn("array", vector_to_array("pValues")).select([col("array")[i].alias(f"{c}_corr") for i, c in enumerate(cols_feature)])

def get_ordinal_corr(spark: SparkSession, df: DataFrame, col_label: str, cols_feature):
    cols_feature_label = [col_label] + cols_feature
    assembler = VectorAssembler(inputCols=[c for c in cols_feature_label], outputCol="category_features")
    pipeline = Pipeline(stages=[assembler])
    pipe = pipeline.fit(df)
    data = pipe.transform(df)

    result = Correlation.corr(data, "category_features", "spearman").head()[0]
    result = [result.toArray().tolist()[0]]
    df = spark.createDataFrame(result,cols_feature_label)
    return df.select(cols_feature)