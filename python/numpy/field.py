import numpy as np

x = np.linspace(0, 2, 100)
r = x.reshape(5, 20)

#%%
shape = r.shape # shows row and column count
ndim = r.ndim
dtype = r.dtype.name
itemsize = r.itemsize
size = r.size
type = type(r)
