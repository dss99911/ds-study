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

plt.show()

# %% hist
# 각 값의 분포도
plt.figure(figsize=(12, 8))
df["values"].hist(bins=5)
plt.title('Histogram of mean term frequency per word over the corpus')
plt.show()
