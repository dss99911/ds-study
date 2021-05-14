from datetime import date, datetime

import numpy as np
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
df_number = pd.DataFrame(np.random.randn(6, 4), index=pd.date_range("20130101", periods=6), columns=list("ABCD"))

# %%
# Select
df_select_column = df["a"]  # get index and column 'a'
df_select_columns = df[["a", "b"]]  # get index and column 'a'
df_select_multiple_column_by_column_index = df[0:3]

df_select_by_filter_columns = df.filter(items=['a', 'b']) # same with df[["a", "b"]]
df_select_by_filter_regex = df.filter(regex='[a-c]') # axis=1 is column
df_select_by_filter_regex2 = df.filter('a') # axis=1 is column

# %%
# New column
df['new_column'] = df['c'].str.lower()