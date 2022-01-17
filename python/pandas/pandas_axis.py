from datetime import date, datetime

import numpy as np
import pandas as pd

dates = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)
#%%

# - index(0) : 각 컬럼 별로, axis인 index를 처음부터 끝까지 반복문으로 체크한다(row를 의미함)
# - columns(1) : 각 인덱스 별로, axis인 columns를 처음부터 끝까지 반복문으로 체크한다(column을 의미함. 1은 기다란 column과 비슷하다고 외우거나, 행렬이 행이 먼저고, 열이 나중이니, 1)
# 특별히 명시하지 않으면, 대부분 index가 기본값. sql에서 select max(a), min(b) 처럼, 한 컬럼의 전체 row를 체크하여, min max구하듯이. row전체를 체크하는게 기본값.
# 기본 값이 columns 인 예외 케이스
#      - filter

# axis를 하나로 합쳐서, 하나의 값을 만들어서, series를 만드는 경우
s_mean_by_column = df_number.mean(axis='index') # 각 컬럼별 평균
s_filter_by_column = df.apply(lambda r: len(str(r[1])) > 1, axis='index') #각 컬럼 별, 1번 row를 체크한다.
s_mean_by_row = df_number.mean(axis='columns') # 각 index별 평균
s_filter_by_row = df.apply(lambda r: r['a'] > 1, axis='columns')  #각 index 별, a column을 체크한다.

# axis 전체를 체크하여, series를 만들어서, dataframe을 만드는 경우,
df_sort_by_index = df_number.sort_index(axis='index', ascending=False) # 각 컬럼 별로 index전체를 체크하여, 정렬한다.
df_filter_by_index = df.filter(like='0', axis='index') # 각 컬럼 별로 index전체를 체크하여, 조건이 성립하는 경우만 남겨 놓는다.
df_sort_by_column = df_number.sort_index(axis='columns', ascending=False) # 컬럼 전체를 각 index 별로 체크하여, 정렬한다ㅣ
df_cumsum_by_column = df_number.apply(np.cumsum)
df_cumsum_by_row = df_number.apply(np.cumsum, axis='columns')

# dataframe과 series를 입력받아, dataframe을 리턴한다.
# axis전체를 체크하기 때문에, axis의 갯수와 동일한 갯수의 series를 입력받는다.
df_subtract = df_number.sub(s, axis='index') # subtraction. index 전체를 체크하며, series와 동일한 index의 값을 뺀다.
