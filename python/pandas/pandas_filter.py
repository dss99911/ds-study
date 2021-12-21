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
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
df_has_nan = df_number.reindex(index=dates[0:4], columns=list(df_number.columns) + ["E"])
df_has_nan.loc[dates[0] : dates[1], "E"] = 1

#%% limit
df_head = df.head()  # first 5 rows
df_tail = df.tail(3)  # last 3 rows

# %% Filtering


df_filter_gt = df[df["a"] > 1]
df_filter_gt2 = df[(df["a"] > 1) & (df["b"] >1)]
df_filter_loc = df.loc[df.loc[:, "a"] > 1]
df_filter_isin = df[df["c"].isin(["string1", "string2"])]
# df_filter_field = df[df > 1] # field side filtering (doesn't remove rows. just show NaN)
df_filter_by_index = df.filter(like='0', axis='index') # axis=0 is row
df_filter_by_index2 = df[0:1] # row[0]
df_filter_by_index3 = df[:2] # row[0,1]
df_filter_by_row_value = df[df['a'] > 1]
df_filter_by_row_value2 = df[df.apply(lambda r: r['a'] > 1, axis='columns')] # axis=1 is column
df_distinct = df.drop_duplicates()
df_distinct_count = df.nunique()
df_distinct_from_series = df["id"].unique()

# Filter by index
Filter_df  = df[df.index.isin("1", "2")]

#%% Filter nan
# https://pandas.pydata.org/docs/user_guide/10min.html#missing-data
# drop rows which has any not number value.
df_filter_nan = df_has_nan.dropna(how="any")
df_fill_nan = df_has_nan.fillna(value=5)
df_is_nan = df_has_nan.isna()