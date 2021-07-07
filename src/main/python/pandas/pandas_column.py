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
#특정 이름의 컬럼이 존재하는지.
exists_a = 'a' in df.columns

#이름 변경
df_new = df.rename(columns={'a': 'new_a'}, index={'b': 'new_b'})

#인덱스 설정
df_index = df.set_index("a")