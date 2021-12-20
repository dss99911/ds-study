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
s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)
#%%
s_dtypes = df.dtypes
field_index = df.index
field_columns = df.columns
field_values = df.values # column명 및 index는 제외한 값만 리턴됨. for문에, 각 컬럼을 사용할 수 있음. ndarray

for a,b,c,d,e in field_values:
    print(f"{a},{b},{c},{d},{e}")

# row와 index
for i, row in df.iterrows():
    print(i, row["a"])

length = len(df) # row size

