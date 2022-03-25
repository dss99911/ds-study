from datetime import date, datetime

import numpy as np
import pandas as pd

dates = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)

# %%
# Select
df_select_column = df["a"]  # get index and column 'a'
# df_select_column2 = df.loc[:, ["f", "b"]] # index나 없는 컬럼 참조시 에러남. Passing list-likes to .loc or [] with any missing labels is no longer supported.
df_select_column = df.a  # get index and column 'a'
df_select_columns = df[["a", "b"]]  # get index and column 'a'
df_select_multiple_column_by_column_index = df[0:3]

df_select_by_filter_columns = df.filter(items=['a', 'b']) # same with df[["a", "b"]]
df_select_by_filter_regex = df.filter(regex='[a-c]') # axis=1 is column
df_select_by_filter_regex2 = df.filter('a') # axis=1 is column

df_select_by_filter_regex2.columns.to_numpy().tolist()

# %%
# New column
df['new_column'] = df.c.str.lower()

# %%
# delete column
del df['a']

df.drop(columns=df.columns[0], inplace=True)  # 기존 df를 변경. delete column, inplace True return None.
df_drop = df.drop(columns=['c'])  # 신규 df를 만듬. return all columns except for the column

# %% Rename column

df_changed_columns = df.copy()
# change whole columns
df_changed_columns.columns = list(map(lambda c: c + "1", df_changed_columns.columns.values))
#%%
#특정 이름의 컬럼이 존재하는지.
exists_a = 'a' in df.columns

#컬럼명 변경하여 새 df생성
df_new = df.rename(columns={'a': 'new_a'}, index={'b': 'new_b'})
#현재의 df의 컬러명 변경
def rename_column(df, suffix=None):
    df.columns = [f"{col}_{suffix}" for col in df.columns.values]
#현재의 df의 컬러명 변경. 컬럼 깊이가 여러개 인 경우.(json을 df로 변환시, 컬럼에 깊이가 여러개 일 수 있음.
def rename_column(df, suffix=None):
    df.columns = [f"{col}_{col2}_{suffix}" for col, col2 in df.columns.values]
df_rename = df.copy()
rename_column(df_rename, "new")

#컬럼 추가
df.loc[:, "test"] = np.abs(df.loc[:, "a"])
df["test2"] = np.abs(df["a"])

#조건있는 컬럼 추가. 조건에 해당 안되면 nan으로 추가됨.
df["test3"] = df["test2"][df["test2"] == 2]
df.loc[df["test2"] == 2, "test4"] = df["test2"]


#%% pop : df에서 column을 제거하고, 해당 column만 있는 dataframe을 리턴한다.
s_a = df.pop("A") # series 리턴