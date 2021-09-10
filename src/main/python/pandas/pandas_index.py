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

#%%

#인덱스 설정
df_index = df.set_index("a") # a 컬럼을 인덱스로 씀

df_index.index = ["r1", "r2", "r3"] # 각 row의 index명을 바꿈

df_reset_index = df_index.reset_index() # 인덱스를 컬럼으로 변환

1 in df_index.index #인덱스가 존재하는지 확인