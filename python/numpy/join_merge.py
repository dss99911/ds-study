import numpy as np
x = np.linspace(0, 2, 100)
r = x.reshape(5, 20)  # row, column
r2 = np.linspace(10, 20, 100).reshape(5, 20)
r3 = np.concatenate((r, r2), axis=1)  # 컬럼을 붙임.(5, 40)
r3 = np.concatenate((r, r2), axis=0)  # row을 붙임.(10, 20)

a, b, c = np.split(r3, [int(.7*len(r3)), int(.85*len(r3))])

#%%

r2h = np.hstack([r, r])  # 컬럼 추가하듯 추가함 (5, 20) => (5, 40)
r2h = np.concatenate((r, r), axis=1)  # 컬럼 추가하듯 추가함 (5, 20) => (5, 40)
r2v = np.vstack([r, r])  # 행 추가하듯 추가함 (5, 20) => (10, 20)
r2v = np.concatenate((r, r), axis=0)  # 행 추가하듯 추가함 (5, 20) => (10, 20)

