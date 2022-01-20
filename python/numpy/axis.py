import numpy as np

arr = np.array([2, 3, 4])
print(arr.shape)
#%% 차원을 늘려준다
row_vec = arr[np.newaxis, :]
print(row_vec.shape)  # (1, 3)

row_vec = arr[:, np.newaxis]
print(row_vec.shape)  # (3, 1)
