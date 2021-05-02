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
df_left = pd.DataFrame({"key": ["foo", "foo"], "lval": [1, 2]})
df_right = pd.DataFrame({"key": ["foo", "foo"], "rval": [4, 5]})
# %%
# Concat
df_append_ignore_index = df.append(df, ignore_index=True)  # index 포함 안함. [0,1,2,3,4,5]
df_append_with_index = df.append(df, ignore_index=True)  # index도 포함하여, append됨. [0,1,2,0,1,2]

# same with union() on spark
df_concat = pd.concat([df_append_ignore_index[:1], df_append_ignore_index[2:3], df_append_ignore_index[4:]])


