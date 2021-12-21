from datetime import date, datetime

import numpy as np
import pandas as pd

dates = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

#%%
df_describe = df_number.describe()

# 누적 수익률등 구할 때 사용. 각 row의 누적 곱
df_cumprod = df_number['A'].cumprod()