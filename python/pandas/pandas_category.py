import numpy as np
import pandas as pd
from pandas import DataFrame

# https://rfriend.tistory.com/404
# 연속적인 값을 카테고리로 만듬

np.random.seed(123)
df = DataFrame({'col_1': np.random.randint(20, size=20),
                'col_2': np.random.randn(20)})

# 동일 길이로 나누어서 범주 만들기(equal-length buckets categorization)
factor_col_1 = pd.cut(df.col_1, 4)

# 카테고리의 구간이 [(-0.019, 4.75] < (4.75, 9.5] < (9.5, 14.25] < (14.25, 19.0]] 로서 4개의 각 구간의 길이가 동일함을 알 수 있습니다.

# 카테고리 구간별 통계를 구함
category_summary = df.col_1.groupby(factor_col_1).agg(['count', 'mean', 'std', 'min', 'max'])
#%%

# pd.qcut() : 동일 개수로 나누어서 범주 만들기 (equal-size buckets categorization)
# labes=False로하면, 범주값이 아닌, 0부터 시작하는 숫자로 범주가 설정됨.
bucket_qcut_col_2_label = pd.qcut(df.col_2, 4)
bucket_qcut_col_2 = pd.qcut(df.col_2, 4, labels=False)
