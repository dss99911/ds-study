import pandas as pd
import numpy as np
import wquantiles
from statsmodels import robust

df_state = pd.read_csv("data/state.csv")

#%% 중심 경향치 https://ko.wikipedia.org/wiki/%EC%A4%91%EC%8B%AC%EA%B2%BD%ED%96%A5%EC%B9%98
from scipy.stats import trim_mean
# 앞뒤 10% 자르고, 평균 내기. 앞뒤에 너무 차이가 나는 오류나 이상 값들을 제외하고 싶은 경우.
mean = df_state['Population'].mean()
mean_t = trim_mean(df_state['Population'], 0.1)
median = df_state['Population'].median()

mean_rate = np.average(df_state['Murder.Rate'])

# weighted mean (가중 평균)
mean_rate_weight = np.average(df_state['Murder.Rate'], weights=df_state['Population'])  # 인구당 가중 확률. 인구가 많으면 좀더 중요하게 다루고 싶은 경우 인듯
# 사용 예: A, B, C 상품 사용자가 각각, 10, 20, 70%이고, 비용이, 1, 2, 3원 일 때, 각 사용자별, 비용 기대 값 = 1 * 0.1 + 2 * 0.2 + 3 * 0.7 = 2.6원

# weighted median (가중 중간값)
median_weight = wquantiles.median(df_state['Murder.Rate'], weights=df_state['Population'])

#%% 변이 추정

std = df_state['Population'].std()  # 표준편차는 특잇값에 민감함
IQR = df_state['Population'].quantile(0.75) - df_state['Population'].quantile(0.25)
MAD = robust.scale.mad(df_state['Population'])  # 중간값 중위 절대 편차. 표준편차보다 robust함

quatines = df_state['Population'].quantile([0.05, 0.25, 0.5, 0.75, 0.90, 0.95])
min = df_state['Population'].min()
max = df_state['Population'].max()

# 도수 분포 표
binnedPopulation = pd.cut(df_state['Population'], 10)
value_counts = binnedPopulation.value_counts()

#%% correlation
sp500_sym = pd.read_csv('data/sp500_sectors.csv')
sp500_px = pd.read_csv("data/sp500_data.csv.gz", index_col=0)
telecomSymbols = sp500_sym[sp500_sym['sector'] == 'telecommunications_services']['symbol']

# Filter data for dates July 2012 through June 2015
telecom = sp500_px.loc[sp500_px.index >= '2012-07-01', telecomSymbols]
print(telecom.corr())

df_points = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [2, 4, 6],
    'y2': [-2, -4, -6]
})
df_points.corr()  # 정확히 직선상에 있으면 1

# correlation by groupby
# 상관계수는 두 컬럼간의 상관 관계를 파악하는데, 보통 여러 외부 요인에 의해 영향을 받는다.
# 집 크기와 tax의 상관 관계를 위치별로 각각 상관관계를 구하면, 더 높은 상관 계수를 얻을 수 있다.
# 값이 적어서 상관계수가 높은 얘들은 쳐내고 확인, 상관계수들의 백분위를 확인해보기
kc_tax = pd.read_csv("data/kc_tax.csv.gz")
kc_tax0 = kc_tax.loc[(kc_tax.TaxAssessedValue < 750000) &
                     (kc_tax.SqFtTotLiving > 100) &
                     (kc_tax.SqFtTotLiving < 3500), :]
grouped = kc_tax0.groupby('ZipCode')

corr_by_zipcode = grouped.apply(lambda x: x.corrwith(x['TaxAssessedValue']))

#%% pivot
# margins=True : 열과 행에 합계를 추가함
df_loan = pd.read_csv("data/lc_loans.csv")
crosstab = df_loan.pivot_table(index='grade', columns='status',
                                aggfunc=lambda x: len(x), margins=True)
print(crosstab)