import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 2, 100)


#%%
fig = plt.figure() # no axes
fig, ax = plt.subplots() # single axes
fig, ax = plt.subplots(2, 2) # 2*2 axes
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.show()

#%%
names = ['group_a', 'group_b', 'group_c']
values = [1, 10, 100]

plt.figure(figsize=(9, 3)) # 가로, 세로 비율

plt.subplot(231) # x축 갯수, y축 갯수, index
plt.bar(names, values)
plt.subplot(232)
plt.scatter(names, values)
plt.subplot(234)
plt.plot(names, values)
plt.suptitle('Categorical Plotting')
plt.show()

#%%
def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.subplot(211)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.show()

#%% multiple plot
# todo 2개가 다 안나옴.
import matplotlib.pyplot as plt
plt.figure(1)                # the first figure
plt.subplot(211)             # the first subplot in the first figure
plt.plot([1, 2, 3])
plt.subplot(212)             # the second subplot in the first figure
plt.plot([4, 5, 6])


plt.figure(2)                # a second figure
plt.plot([4, 5, 6])          # creates a subplot() by default

plt.figure(1)                # figure 1 current; subplot(212) still current
plt.subplot(211)             # make subplot(211) in figure1 current
plt.title('Easy as 1, 2, 3') # subplot 211 title

#%% OO-style : for non-interactive plotting

# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
fig, ax = plt.subplots()  # Create a figure and an axes.
ax.plot(x, x, label='linear')  # Plot some data on the axes.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
fig.show()


#%% pyplot style : for interactive plotting
# - 하나의 axes만 있는 듯? 그래서, 간편하게, 하나의 통계치를 보고 싶을 때, axes를 정의하지 않고, 사용.
plt.ion()
plt.plot(x, x, label='linear')  # Plot some data on the (implicit) axes.
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.show()# 현재의 axes위에 추가로 그린 후, 캐시를 삭제해서, 다음에 그릴 때, 추가로 그리지 않고, 새로 그리게 한다.
