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

#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html

df = pd.DataFrame({
    'num': np.arange(3) + 2,
    'years': ['2018', '2019', '2020'],
    'values': [1, 2, 3],

})
df.plot()  # 직선. x: index, y: all numeric columns
df.plot(kind='bar')  # bar
df.plot(x="years", y="values", kind='bar', figsize=(10, 5))  # x, y column
ax = df.plot.bar(figsize=(4, 4), legend=False)  # pie차트는 어떠한 경우에도 권장되지 않는다고..
ax.set_xlabel('Cause of delay')
ax.set_ylabel('Count')

plt.show()
