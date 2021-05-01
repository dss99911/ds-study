# Init
# https://pandas.pydata.org/docs/user_guide/10min.html#min
import numpy as np
import pandas as pd
from datetime import date, datetime

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
df_number = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=df_create_dates, columns=list("ABCD"))
# %%
# Self Create

df_create_list = pd.Series([1, 3, 5, np.nan, 6, 8])
df_create_dates = pd.date_range("20130101", periods=6)
df_create_dataframe_index_column = pd.DataFrame(np.random.randn(6, 4), index=df_create_dates, columns=list("ABCD"))
df_create_dataframe_1 = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
df_create_dataframe_2 = pd.DataFrame(
    {
        "A": 1.0,
        "B": pd.Timestamp("20130102"),
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train"]),
        "F": "foo",
    }
)
# %%
# Read

df_from_parquet = pd.read_parquet("path")
df_from_csv = pd.read_csv("path")

# %%
# Dataframe functions, fields
df_field_dtypes = df.dtypes
df_field_head = df.head()
df_field_tail = df.tail(3)
df_field_index = df.index
df_field_columns = df.columns
df_field_describe = df.describe()
df_field_transpose = df.T  # convert column and row
df_field_copy = df.copy()
# %%
# Numpy

df_numpy = df.to_numpy()

# %%
# Sort
df_sort_by_index = df.sort_index(axis=1, ascending=False)
df_sort_by_value = df.sort_values(by="b")

# %%
# Select
df_select_column = df["a"]  # get index and column 'A'
df_select_columns = df[["a", "b"]]  # get index and column 'A'
df_select_multiple_column = df[0:3]
df_select_add_column = df.copy()
df_select_add_column = df["f"] = ["one", "one", "two"]
# %%
# Location, find values by selecting the scope of the rows and columns
df_loc = df.loc[0]  # get fields of a row index
df_loc_multi_scope = df.loc[0:2, ["a", "b"]]  # select by row index and columns
df_loc_all_rows_some_columns = df.loc[:, ["a", "b"]]  # select columns of all rows
df_loc_single_value = df.loc[0, "a"]  # get specific value
df_loc_single_value2 = df.at[0, "a"]  # get specific value(equivalent to the prior method
# index location. this is just by index number
df_iloc = df.iloc[2] # 3rd row
df_iloc1 = df.iloc[0:2, 0:2]
df_iloc2 = df.iloc[[0, 2], [0, 2]]
df_iat = df.iat[1, 1]

# Location Setting
df.at[0, "a"] = 0
df.iat[0, 1] = 0
df.loc[:, "D"] = np.array([5] * len(df))
df_number[df_number > 0] = -df_number # change sign of number
# %%
# Filtering
df_filter_gt = df[df["a"] > 1]
df_filter_isin = df[df["c"].isin(["string1", "string2"])]
# df_filter_field = df[df > 1] # field side filtering (doesn't remove rows. just show NaN)

# %%
# TODO study from https://pandas.pydata.org/docs/user_guide/10min.html#missing-data