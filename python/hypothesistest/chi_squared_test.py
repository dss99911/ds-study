# # https://velog.io/@gayeon/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EB%B6%84%EC%84%9D-%EC%B4%88%EB%B3%B4%EC%9E%90%EB%A5%BC-%EC%9C%84%ED%95%9C-T-test-Chi-squared-test
# T-test는 표본집단의 평균을 비교할 때 선택하는 방법이었다면,
# Chi-squared test는 표본집단의 분포를 비교할 때 선택하는 방법이다.
# 다만, Chi-squared test는 categorical data에 대해서만 사용이 가능하다.
# Chi-squared test도 sample의 개수에 따라 one-sample Chi-squared test와 two sample Chi-squared test로 나뉜다.


# 필요한 패키지 import
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats

# 데이터셋 불러오기
df = sns.load_dataset("penguins")
df = df.dropna()

# 데이터 프레임 column명 수정
df = df.rename(columns={"species":"species", "island":"island", "bill_length_mm":"bill_length", "bill_depth_mm":"bill_depth",
                        "flipper_length_mm":"flipper_length", "body_mass_g":"body_mass", "sex":"sex"})

#%% one sample Chi-squared test
# one sample Chi-squared test은 서론에서 말했던 "이 주사위는 공평한 주사위이다."에 대한 검정처럼,
# 데이터의 분포가 예상과 같은지 확인할 때 사용한다.
# 귀무가설: 펭귄의 성비는 1:1일 것이다.
# 대립가설: 펭귄의 성비는 1:1이 아닐 것이다.
# 신뢰도: 95%

male = df["sex"].value_counts()["Male"]
female = df["sex"].value_counts()["Female"]
exp = len(df)/2
stats.chisquare(f_obs=[male, female], f_exp=[exp, exp])
# p-value가 0.05보다 크므로 귀무가설을 기각할 수 없다. 따라서, 펭귄의 성비는 1:1이다.


#%% two sample Chi-squared test
# two sample Chi-squared test는 두 표본집단의 분포가 동일한지 확인할 때 사용한다.
# 즉, 두 표본집단이 연관이 있는지, 없는지를 확인할 수 있다.
# 두 표본집단을 crosstab 형식으로 제공해야 하고, 결과값이 작으면 상관관계가 있고, 크면, 상관 관계가 없다.

# 펭귄의 몸무게와 플리퍼 길이는 관련이 있지 않을까?
# two sample Chi-squared test를 사용하면 "펭귄의 몸무게와 플리퍼 길이는 독립이다."라는 가설을 검정할 수 있다.
# 단, 여기서 주의해야 할 점은 Chi-squared test는 categorical data에만 사용할 수 있다는 점이다.
# 우리가 가지고 있는 데이터셋에서는 펭귄의 몸무게와 플리퍼 길이가 continuous data이다.
# 따라서 펭귄의 몸무게와 플리퍼 길이에 대한 Chi-squared test를 시행하려면
# 먼저 데이터를 categorical data로 바꿔줘야 한다.

mass_cut = pd.cut(df.body_mass, 3)
flipper_cut = pd.cut(df.flipper_length, 3)
data = pd.crosstab(mass_cut, flipper_cut)
data.columns = ["Short", "Middle", "Long"]
data.index = ["Light", "Middle", "Heavy"]

# 몸무게와 플리퍼 길이를 각각 세 그룹으로 나누고, 그 결과를 crosstab으로 만들었다.
# 이제 펭귄의 몸무게와 플리퍼 길이에 대해서 two sample Chi-squared test를 시행할 수 있다.
#
# 귀무가설: 펭귄의 몸무게와 플리퍼 길이는 연관이 없다.
# 대립가설: 펭귄의 몸무게와 플리퍼 길이는 연관이 있다.
# 신뢰도: 95%
chi, pvalue, _, _ = stats.chi2_contingency(data, correction=False)

# p-value가 0.05보다 작기 때문에 귀무가설을 기각하고 대립가설을 채택한다. 따라서 펭귄의 몸무게와 플리퍼 길이는 연관이 있다.