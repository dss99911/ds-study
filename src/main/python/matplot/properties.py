import matplotlib.pyplot as plt
import numpy as np

#%% properties
# Line 2D properties : https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D

# default : blue line "b-". 좌표들을 선으로 연결한다.
plt.plot([5,4,3,2,1], "ro") # red with 'o' marker(without line)
plt.plot([5,4,3,2,1], "b--") # blue with dash line
plt.plot([1,1,1,1,1], "g^") # green with '^' marker

# arguments by dictionary
plt.plot([1, 2, 3, 4], **{"marker":"x"})

# marker
plt.plot([5, 2, 3, 4], marker="x")
plt.plot([1, 4, 2, 3], marker="o")

# 선 두께
plt.plot([1, 4, 2, 3], linewidth=2.0)

# legend
plt.plot([5, 2, 3, 4], label="a")
plt.plot([1, 4, 2, 3], label="b")
plt.legend()

# turn off antialiasing
line, = plt.plot([1, 5, 1, 5])
line.set_antialiased(False)

plt.show()

#%% 그래프의 부속 설정
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# the histogram of the data
n, bins, patches = plt.hist(x, 50, density=1, facecolor='g', alpha=0.75)

plt.xlabel('Smarts', fontsize=14, color='red')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$') # 특정 위치에 텍스트 추가
plt.axis([40, 160, 0, 0.03])  # x축 범위 0~6, y축 범위 0~20
plt.grid(True)
plt.show()

#%% Annotation
ax = plt.subplot()

t = np.arange(0.0, 5.0, 0.01)
s = np.cos(2*np.pi*t)
line, = plt.plot(t, s, lw=2)

plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )

plt.ylim(-2, 2)
plt.show()

#%% axis scale

# Fixing random state for reproducibility
np.random.seed(19680801)

# make up some data in the open interval (0, 1)
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = np.arange(len(y))

# plot with various axes scales
plt.figure()

# linear
plt.subplot(221)
plt.plot(x, y)
plt.yscale('linear')
plt.title('linear')
plt.grid(True)

# log
plt.subplot(222)
plt.plot(x, y)
plt.yscale('log')
plt.title('log')
plt.grid(True)

# symmetric log
plt.subplot(223)
plt.plot(x, y - y.mean())
plt.yscale('symlog', linthresh=0.01)
plt.title('symlog')
plt.grid(True)

# logit
plt.subplot(224)
plt.plot(x, y)
plt.yscale('logit')
plt.title('logit')
plt.grid(True)
# Adjust the subplot layout, because the logit one may take more space
# than usual, due to y-tick labels like "1 - 10^{-3}"
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)

plt.show()