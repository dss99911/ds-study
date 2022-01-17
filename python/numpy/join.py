import numpy as np
x = np.linspace(0, 2, 100)
r = x.reshape(5, 20)  # row, column
r2 = np.linspace(10, 20, 100).reshape(5, 20)
r3 = np.concatenate((r, r2), axis=1)  # 컬럼을 붙임.(5, 40)
r3 = np.concatenate((r, r2), axis=0)  # row을 붙임.(10, 20)

a, b, c = np.split(r3, [int(.7*len(r3)), int(.85*len(r3))])