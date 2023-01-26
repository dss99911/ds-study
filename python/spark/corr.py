from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import ChiSquareTest
from pyspark.ml.stat import Correlation
from pyspark.ml.functions import *
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import *


def get_numeric_corr(df: DataFrame, cols_feature, col_label: str):
    corrs = list(map(lambda c: corr(col_label, c).alias(f"{c}_corr"),cols_feature))
    return df.select(*corrs)

def get_categorical_corr(df: DataFrame, cols_feature, col_label: str):
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

def get_ordinal_corr(spark: SparkSession, df: DataFrame, cols_feature, col_label: str):
    cols_feature_label = [col_label] + cols_feature
    assembler = VectorAssembler(inputCols=[c for c in cols_feature_label], outputCol="category_features")
    pipeline = Pipeline(stages=[assembler])
    pipe = pipeline.fit(df)
    data = pipe.transform(df)

    result = Correlation.corr(data, "category_features", "spearman").head()[0]
    result = [result.toArray().tolist()[0]]
    df = spark.createDataFrame(result,cols_feature_label)
    return df.select(cols_feature)


def show_corr(df, count=300):
    ret = change_double_format(df)

    spark.createDataFrame(ret.toPandas().T.reset_index(), ["feature_name", "corr"]) \
        .sort(abs(col("corr")).desc()) \
        .show(count, False)

def crosstab_ratio(df, feature, label):
    df = df.stat.crosstab(label, feature)
    columns = df.columns[1:]
    df_sum = df.groupBy().sum() \
        .toDF(*list(map(lambda c: f"sum_{c}", columns)))
    df_cross = df.crossJoin(df_sum)
    for c in columns:
        df_cross = df_cross.withColumn(f"ratio_{c}", col(c) / col(f"sum_{c}"))
        df_cross = df_cross.drop(f"sum_{c}")
    return df_cross

def change_double_format(df):
    for f in df.schema.fields:
        if f.dataType.__class__ != DoubleType:
            continue
        df = df.withColumn(f.name, format_number(f.name, 10))
    return df