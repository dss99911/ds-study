from datetime import date, datetime
import numpy as np
import pandas as pd
from pandas import DataFrame

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
df_number = pd.DataFrame(np.random.randn(6, 4), index=pd.date_range("20130101", periods=6), columns=list("ABCD"))

#%%

# series = df[str] : 컬럼 a만 있는 Series를 가져온다 (컬럼을 하나만 입력하면, Series를 리턴하고, 여러개면, Dataframe을 리턴한다)
series_one_column = df["a"]

# df<selected-columns> = df[array<str>]
df_two_column = df[["a", "b"]]

# Series<bool> = series with condition operator : series의 각 값이 1보다 큰지 여부의 값을 Series로 만든다.
series_boolean = series_one_column > 1

# Dataframe<bool> = dataframe with condition operator : series의 각 값이 1보다 큰지 여부의 값을 Series로 만든다.
df_boolean = df_number > 0

# df<all-columns> = df[series<bool>] : 각 row를 포함할지 여부를 series로 받아서, True인 row만 포함한 Dataframe을 만든다.
df_filter = df[series_boolean]

# df<only-valid-value> = df[df<bool>] : True인 필드만 보여주고, 그 외에는 nan으로 보여줌
df_filter_per_value = df_number[df_boolean]

#%%
# set value on a column
df["f"] = ["one", "one", "two"]
df.loc[:, "D"] = [5] * len(df) # set array
df.loc[:, "D"] = pd.Series([5] * len(df)) # set Series
df.loc[:, "D"] = np.array([5] * len(df)) # set numpy array

# set value on a row
df.loc[3] = [5] * len(df.columns) # set array
# df.loc[3] = pd.Series([5] * len(df.columns)) # This is not supported
df.loc[3] = pd.Series({'a': 1, 'b': 5, 'c': 2, 'd': 3}) # Series just with array is not supported
df.loc[3] = np.array([5] * len(df.columns)) # set array
df_number[df_number > 0] = -df_number # change value of same column, row index in -df_number