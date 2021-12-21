import numpy as np

x = np.linspace(0, 2, 100)
xy = x.reshape(5, 20)
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
a22 = np.floor(10 * np.random.random((2,2)))
b22 = np.floor(10 * np.random.random((2,2)))
# %% operator

x_add_2 = x + 2 # x*2
x_add_array = x + x_add_2
x_multiply_2 = x * 2 # x*2
x_square_2 = x ** 2 # x^2
y_abs = np.abs(y)
x_add_2 += 1

#%% filter
y_filter_condition = y[(y > 0) & (y < 1)]

#%% where, when~otherwise
x_where = np.where(x > 0.1, x, 0)

#%% sort
y.sort() # y is sorted.

#%% reshape
r = x.reshape(5, 20)
r.resize((20, 5)) # resize change the array. reshape return new changed array

for element in r.flat: # make flat array for iterator
    print(element)
x2 = r.ravel() # make flat array
transpose = r.T # tanspose
r2 = r.reshape(2, -1) # if -1. it's automatically calculated

v = np.vstack((a22, b22))# 세로로 배열 추가
h = np.hstack((a22, b22))# 가로로 배열 추가
c = np.column_stack((np.array([4., 2.]), np.array([1., 3.])))# 컬럼 추가하듯이 추가

#%% get from index
x[2]
x[2:5]
x[:10:2] = 10 # from 0 to 10, increase 2. and set 10
xy[:2, 5:6]