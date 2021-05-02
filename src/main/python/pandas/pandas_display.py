from datetime import date, datetime

import numpy as np
import pandas as pd

dates = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
#%%
pd.options.display.float_format = '${:,.2f}'.format
print(df_number)
str = df_number.to_string()