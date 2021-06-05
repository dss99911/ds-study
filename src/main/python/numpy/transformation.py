import numpy as np

x = np.linspace(0, 2, 100)
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
# %% operator

x_add_2 = x + 2 # x*2
x_add_array = x + x_add_2
x_multiply_2 = x * 2 # x*2
x_square_2 = x ** 2 # x^2
y_abs = np.abs(y)

#%% filter
y_filter_condition = y[(y > 0) & (y < 1)]

#%% sort
y.sort() # y is sorted.