import numpy as np
import pandas as pd

s = pd.Series(["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"])
s_num = pd.Series([1,2,3])

s_array = pd.Series([np.ndarray(shape=(1, 3), buffer=np.array([1,2,3]), dtype=int),np.ndarray(shape=(1, 3), buffer=np.array([1,2,3]), dtype=int),np.ndarray(shape=(1, 3), buffer=np.array([1,2,3]), dtype=int)])

#%%

s_lower = s.str.lower()
mean = s_num.mean()
mean_array = s_array.mean() # ndarray의 경우, array의 각 item당 평균을 구함.
#%%
# Series을 Dataframe으로 변환
df = s_lower.to_frame()

# Series 컬럼명 변경
s_lower.rename("new_name").to_frame()

#%%
#%% map
list_a = s.map(lambda c: f"c{c}").tolist()