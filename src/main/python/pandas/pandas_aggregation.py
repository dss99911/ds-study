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

# group by time
df_sp = pd.read_csv("data/SP500_NOV2019_Hist.csv", index_col=0, parse_dates=True)
s_open = df_sp["Open"].groupby(pd.Grouper(freq="1H")).first()

# 여러 컬럼을 시간으로 그룹핑 하기
df_resample = df_sp.resample("1H").agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
df_group_time = df_sp.groupby(pd.Grouper(freq="1H")).agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})

# 그룹핑 없이 전체를 agg하기. (True대신에 다른 키값을 입력해도 됨. 하지만 동일한 값을 넣어야 전체가 그룹핑됨.
# 커스텀 조건에 따라 그룹핑하는 것도 가능
df_sp.groupby(lambda _: True).agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})

#%% Rolling
# 해당 row 및 앞 4개 row의 평균
df.rolling(5).mean()