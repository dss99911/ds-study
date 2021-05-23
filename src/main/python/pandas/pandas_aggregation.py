from datetime import date, datetime

import numpy as np
import pandas as pd

dates = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
df_digit = pd.Series(np.random.randint(0, 7, size=10))
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)
#%%

# mean per each column
s_mean_by_columns = df_number.mean()
s_mean_by_rows = df_number.mean(axis=1)
s_sum_by_columns = df_number.sum()
s_value_counts = df_digit.value_counts()

#%% Group by

df_groupby_sum = df.groupby("A").sum() # 합산이 불가한 "B"컬럼은 제외하고 합산한다.
df.groupby(["A", "B"]).sum()

#%% Rolling
# 해당 row 및 앞 4개 row의 평균
df.rolling(5).mean()