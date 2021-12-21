import json
from datetime import date, datetime

import numpy as np
import pandas as pd
from pandas import json_normalize

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

# %%

s_lower = df['c'].str.lower()
s_slice = df['c'].str.slice(-4)
s_len = df['c'].str.len()
df['new_column'] = s_lower

# regex
df["c"].str.extract(r'(^.{5})')

#%% equal

equals = df['new_column'] == df['new_column']

#%% isin
isin = np.isin(df['new_column'], ["a", "b"])
#%% json
json_data = "{\"a\": {\"b\":2}, \"c\":1}"
# json_data = "{\"a\": [1,2,3]}"
dict_data = json.loads(json_data) # return dict
df_data = json_normalize(dict_data) # return DataFrame
