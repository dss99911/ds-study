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
df_left = pd.DataFrame({"key": ["foo", "foo2", "foo2"], "lval": [1, 2, 2]})
df_right = pd.DataFrame({"key": ["foo2", "foo"], "rval": [4, 5]})
df_right1 = pd.DataFrame({"key": ["foo"], "rval": [5]})
df_right2 = pd.DataFrame({"key": ["foo", "foo"], "rval": [4, 5]})

#%% append
df_left.append({"key": "foo3", "lval": 1}, ignore_index=True)

# %% Merge
df_merge = pd.merge(df_left, df_right, on="key")
# df_merge = pd.merge(df_left, df_right, on=["key","lval"]) #2개 컬럼 조인
df_merge2 = pd.merge(df_left, df_right2, on="key", how="left")

# join by index.
df_merge3 = df_left.merge(df_right1, how="left", left_index=True, right_index=True)
# join by index and column
df_merge4 = df_left.merge(df_right1.set_index("key"), how="left", left_on="key", right_index=True)

#%% Concate
df1 = df
df2 = df

#upsert
df_upsert = pd.concat([df1[~df1.index.isin(df2.index)], df2])
#just concat rows
df_plus = pd.concat([df, df])

#concat columns, if index is not matched. the value is nan
# index가 중복될 경우 에러 발생.
# ValueError: Shape of passed values is (3, 2), indices imply (2, 2)
df_concat2 = pd.concat([df_left.set_index("key"), df_right1.set_index("key")], axis=1)

#%%
combine = df["a"].combine_first(df["b"])  # 첫 df에 null인 값이 있으면, 두번째 df의 값을 사용.