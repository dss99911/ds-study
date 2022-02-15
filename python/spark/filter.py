from util.util import *


def filters(df: DataFrame):
    df.filter(df.a == 1)
    df.filter(df["a"] == 1)
    df.filter(col("a") == 1)
    df.filter((col("a") == 1) & (df.b == 1))
    df.filter((col("a") == 1) | (df.b == 1))