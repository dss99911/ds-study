
import numpy as np
import pandas as pd

s = pd.Series(["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"])

#%%

s_lower = s.str.lower()

#%%
# Series을 Dataframe으로 변환
df = s_lower.to_frame()