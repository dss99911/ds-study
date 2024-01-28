# https://pandas.pydata.org/docs/user_guide/sparse.html
# sparse vector는 하나의 컬럼의 필드에, 존재하는 데이터 값을 리스트 처럼 관리한다면(여러 컬럼을 하나의 sparse vector 컬럼으로 관리)
# pandas sparse의 경우, 하나의 컬럼의 전체 row를 sparse로 관리하는 형식
import numpy as np
import pandas as np

arr = np.random.randn(10)
arr[2:-2] = np.nan

ts = pd.Series(pd.arrays.SparseArray(arr))

ts