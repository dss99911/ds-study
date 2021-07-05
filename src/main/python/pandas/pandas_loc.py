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
dates = pd.date_range("20130101", periods=6)
r = np.random.randn(6, 4)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

# %%
# Location, find values by selecting the scope of the rows and columns
# loc[row, column]
series_loc = df.loc[0]  # get fields of a row index
df_loc_date_index = df_number.loc['2013'] # get rows with date like
df_loc_date_index2 = df_number.sort_index().loc["2021-07-05T01:11":"2021-07-05T01:16"] # get rows with date like
df_loc_date_index3 = df_number.sort_index().loc[datetime(2021,7,5,1,11):datetime(2021,7,5,1,16)]
df_loc_multi_scope = df.loc[0:2, ["a", "b"]]  # select by row index and columns
df_loc_all_rows_some_columns = df.loc[:, ["a", "b"]]  # select columns of all rows
df_loc_single_value = df.loc[0, "a"]  # get specific value
df_loc_single_value2 = df.at[0, "a"]  # get specific value(equivalent to the prior method
# index location. this is just by index number
df_iloc = df.iloc[2]  # 3rd row
df_iloc1 = df.iloc[0:2, 0:2]
df_iloc2 = df.iloc[[0, 2], [0, 2]]
df_iat = df.iat[1, 1]

df_reindex = df_number.reindex(index=dates[0:2], columns=list(df_number.columns) + ["E"])

#find in index
index_exists = 'g' in df.index
# %%
# Location Setting
df["f"] = ["one", "one", "two"] # set a column
df.at[0, "a"] = 0
df.iat[0, 1] = 0
df.loc[:, "D"] = [5] * len(df) # set array
df.loc[:, "D"] = pd.Series([5] * len(df)) # set Series
df.loc[:, "D"] = np.array([5] * len(df))
df.loc[3] = pd.Series({'a': 1, 'b': 5, 'c': 2, 'd': 3})
df_number.loc[dates[0] : dates[1], "E"] = 1

df_minus = -df_number

df_number[df_number > 0] = -df_number  # change sign of number for positive number only
