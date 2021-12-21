from datetime import date, datetime

import matplotlib.pyplot as plt
import pandas as pd


df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})

df.plot(kind='bar')
plt.xticks(
    ticks=range(len(df)),
    labels=df['a']
)

plt.show()
# %% pandas plot

import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame({
    'num': np.arange(3) + 1,
    'values2': [1, 2, 3],
    'years': ['2018', '2019', '2020'],

})
df.plot(x="years", y="values2", kind='bar')


plt.show()
