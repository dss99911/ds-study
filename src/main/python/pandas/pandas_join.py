# https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html

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
df_left = pd.DataFrame({"key": ["foo", "foo2"], "lval": [1, 2]})
df_right = pd.DataFrame({"key": ["foo2", "foo"], "rval": [4, 5]})
df_right2 = pd.DataFrame({"key": ["foo"], "rval": [4]})

# %% Merge
df_merge = pd.merge(df_left, df_right, on="key")
df_merge2 = pd.merge(df_left, df_right2, on="key", how="left")

#%% Concate
df1 = df
df2 = df

#upsert
df_concat = pd.concat([df1[~df1.index.isin(df2.index)], df2])
#just concat rows
df_plus = pd.concat([df, df])
