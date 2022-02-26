from datetime import date, datetime

import numpy as np
import pandas as pd

dates = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
df_digit = pd.Series(np.random.randint(0, 7, size=10))
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo", "food"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three", None],
        "C": [0, 1, 1, 2, 3, 3, 4, 4, 5],
        "D": np.random.randn(9),
    }
)

#%%

# groupBy를 하면, 해당 컬럼이 index가 됨
df_groupby_sum_count = df.groupby(["A", "B"])["C"].agg(["sum", "count"])

df_groupby_sum_count_dict = df.groupby(["A", "B"]).agg({
        "C": ["sum", "count"],
        "D": [pd.Series.nunique]
})

# index를 column으로 변환 pivot과 동일. groupBy("A").pivot("B").agg(sum("C"), count("C")) 와 동일
df_groupby_sum_count_dict2 = df_groupby_sum_count_dict.unstack("B")

# agg시, agg function name과 column name이 tuple로 되어 있는 듯
for col_name, agg_name in df_groupby_sum_count_dict.columns.values:
    print(col_name, agg_name)

#%%

# mean per each column
s_mean_by_columns = df_number.mean()
s_mean_by_rows = df_number.mean(axis=1)
s_sum_by_columns = df_number.sum()

# mean for a column
df_number["A"].mean()
# min's index for a column
df_number["A"].idxmin()

# 한 컬럼의 각 값들의 count를 구하기(groupby(column).count())
s_value_counts = df_digit.value_counts()

#%% Group by
#group의 값이 null이면 해당 값은 제외됨
df.loc[3, "C"] = None

df_groupby_sum = df.groupby("A").sum() # 합산이 불가한 "B"컬럼은 제외하고 합산한다.
df_groupby_sum2 = df.groupby(["A", "B"]).sum()
df_groupby_sum2_index_to_column = df_groupby_sum2.reset_index()
df_groupby_sum1 = df.groupby(["A", "B"])["C"].sum()


# C의 값이 널이면, count에 포함 안됨
df_groupby_sum_count = df.groupby(["A", "B"])["C"].agg(["sum", "count"])

df["A"].value_counts()  # A의 각 값별 count

# group by time
df_sp = pd.read_csv("data/SP500_NOV2019_Hist.csv", index_col=0, parse_dates=True)
s_open = df_sp["Open"].groupby(pd.Grouper(freq="1H")).first()

# 여러 컬럼을 시간으로 그룹핑 하기
df_resample = df_sp.resample("1H").agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
df_group_time = df_sp.groupby(pd.Grouper(freq="1H")).agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
df_resample_multiple_agg = df_sp.resample("1H").agg({'Open': ['first', 'max'], 'High': ['first', 'max']})
for a1, b in df_resample_multiple_agg.columns.values:
    #컬럼이 (Open, first) 형식으 로 되어 있다.
    print(f"{a1} : {b}")

df_sp.agg({
    'Open': pd.Series.nunique
})

# 그룹핑 없이 전체를 agg하기. (True대신에 다른 키값을 입력해도 됨. 하지만 동일한 값을 넣어야 전체가 그룹핑됨.
# 커스텀 조건에 따라 그룹핑하는 것도 가능
df_sp.groupby(lambda _: True).agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})


# sum()은 그룹핑 없이도 가능.
df.isnull().sum()

# group by index number
a = df.set_index(["A", "B"]).groupby(level=0).count()

#%% Windows

# rank

# df_groupby_sum_count["rank"] = (
#         df_groupby_sum_count
#         .reset_index()
#         .groupby("A")["sum"]
#         .rank(ascending=False, method="min")  # method 기본값은 average. 동일한 값이 여러개 있을 때, 맨앞과 맨 뒤 rank의 평균을 구함
#         # .rank(ascending=False, method="first")  # row_number와 동일
#         .values.astype(np.int64) - 1
# )

# rank sort by C, D
df["rank"] = (
        df.sort_values(['D', 'B'])
        .groupby("A").C
        .rank(ascending=False, method="first").astype(int) - 1
)

#%% Rolling
# 해당 row 및 앞 4개 row의 평균
df.rolling(5).mean()