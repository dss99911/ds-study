import matplotlib.pyplot as plt
import numpy as np

# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html#matplotlib.pyplot.hist

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# the histogram of the data
# x값을 50개로 나눠서, 각 범위별로 반도수 구하기
# density는 probability density를 구할 때. False이면, 단순 count를 구함.
n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()


# %% hist
# 각 값의 분포도
# plt.figure(figsize=(12, 8))
import pandas as pd

df = pd.DataFrame({
    'num': np.arange(3) + 2,
    'years': ['2018', '2019', '2020'],
    'values': [1, 2, 3],

})

df["values"].hist(bins=5, density=True, figsize=(12, 8))  # density : 갯수가 아닌 밀도로 표시
plt.title('Histogram of mean term frequency per word over the corpus')
plt.show()

#
state = pd.read_csv("data/state.csv")
ax = state['Murder.Rate'].plot.hist(density=True, xlim=[0, 12],  # xlim : x축의 범위 정함
                                    bins=range(1, 12), figsize=(4, 4))  #bin에 구체적 범위값을 넣으면, 소수점 없이 정확히 분할함
state['Murder.Rate'].plot.density(ax=ax)  # density 그래프(histogram의 부드러운 버전)를 ax 위에 그림. 단위가 밀도이므로 density=True필요
ax.set_xlabel('Murder Rate (per 100,000)')

plt.tight_layout()
plt.show()
