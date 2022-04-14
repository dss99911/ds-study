from datetime import datetime, date
from spark.util.util import *

spark = SparkSession.builder.getOrCreate()

spark_df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0)),
    Row(a=4, b=5., c='String3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])
spark_df.summary().show()

#+-------+------------------+------------------+-------+
#|summary|                 a|                 b|      c|
#+-------+------------------+------------------+-------+
#|  count|                 3|                 3|      3|
#|   mean|2.3333333333333335|3.3333333333333335|   null|
#| stddev|1.5275252316519468|1.5275252316519468|   null|
#|    min|                 1|               2.0|string1|
#|    25%|                 1|               2.0|   null|
#|    50%|                 2|               3.0|   null|
#|    75%|                 4|               5.0|   null|
#|    max|                 4|               5.0|string3|
#+-------+------------------+------------------+-------+


# get_dummies
def get_dummies(df: DataFrame, columns):
    other_cols = list(map(lambda c: col(c), set(df.columns) - set(columns)))
    new_cols = []
    categories = df.agg(*[collect_set(clean_column_name(c)).alias(c) for c in columns]).collect()[0].asDict()
    for c in columns:
        for cat in categories[c]:
            new_cols.append(when(clean_column_name(c) == cat, 1).otherwise(0).alias(f"{c}_{cat}"))
    df = df.select(other_cols + new_cols)
    return df


def clean_column_name(c):
    """저장할 때, 컬럼명 제약이 있음. 대소문자는 구분 안하므로 편의상 소문자로 처리 (spark.sql.caseSensitive default가 False)
    같은 값인데, 대소문자가 다른 경우에 동일하게 처리할지 여부는 get_dummies이전 처리에서 결정하는게 좋음. 이 경우, lower()없애기"""
    return regexp_replace(lower(c), "[\\. ,;\\{\\}\\(\\)\n\t=]", "_")

get_dummies(spark_df, ['b', 'c']).show()