from util.util import *


def joins(df: DataFrame, df2: DataFrame):


    df.join(df2, how='left', on=['a'])
    df.join(df2, (df.a == df2.a) & (df.b == df2.b))  # 이거 안되는 듯? 버전 문제인가?
    df.join(df2, (df["a"] == df2["a"]) & (df["b"] == df2["b"]))

    df.alias("a").join(df2.alias("b"), (col("a.a") == col("b.a") & col("a.b") == col("b.b")))\
        .select(list(map(lambda c: f"a.{c}", df.columns)) + ["b_column"])