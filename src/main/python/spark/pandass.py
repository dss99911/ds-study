from datetime import date, datetime

import pandas as pd


def from_object():
    """# https://spark.apache.org/docs/latest/api/python/user_guide/arrow_pandas.html"""
    pd.DataFrame({
        'a': [1, 2, 3],
        'b': [2., 3., 4.],
        'c': ['string1', 'string2', 'string3'],
        'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
        'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
    })


def from_parquet():
    pd.read_parquet("path")


def from_csv():
    pd.read_csv("path")
