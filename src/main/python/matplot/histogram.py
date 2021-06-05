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

#%%