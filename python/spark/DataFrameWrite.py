from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row
from pyspark.sql import SparkSession
from DataFrameRead import *
spark = SparkSession.builder.getOrCreate()


def write_to_excel(df, path):
    """
    pip install xlsxwriter for writing
    https://xlsxwriter.readthedocs.io/contents.html
    """

    pandas_df = df.toPandas()
    # Exporting pandas dataframe to xlsx file
    pandas_df.to_excel(path, engine='xlsxwriter')


def collect_rows(df: DataFrame):
    l: list[Row] = df.collect()
    a: list[str] = df.select("a").rdd.flatMap(lambda x: x).collect()  # select single column
    all: list[dict] = df.rdd.map(lambda r: r.asDict()).collect()  # select multiple columns
    for row in df.toLocalIterator():
        row["a"]

    for a, b, c in df.toLocalIterator():
        pass

    a, b, c = df.first()  # column index 0, 1, 2

if __name__ == '__main__':
    df = write_to_excel(create_by_row(), 'excel_test.xlsx')
    df.show()
    df.printSchema()
