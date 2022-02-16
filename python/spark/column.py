from spark.util.util import *
from spark.read import create_by_row


#add column
def add_column(df):
    df.withColumn('col_name', lit("1"))


#remove column
def remove_column(df):
    df = df.drop('col_name')
    return df


#select column
def select_column(df):
    c = ["b", "c"]
    d = ["d", "e"]
    df.select("a", *c, *d)
    df.select(["a", "b"])


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

if __name__ == '__main__':
    rename_columns_by_list(create_by_row(), ["test", "test2", "test3", "test4", "test5"]).show()

    rename_columns_by_name(create_by_row(), lambda c: "col_" + c, exclude=["a"]).show()