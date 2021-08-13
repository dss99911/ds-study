# 필요한 패키지 import
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats

# https://velog.io/@gayeon/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EB%B6%84%EC%84%9D-%EC%B4%88%EB%B3%B4%EC%9E%90%EB%A5%BC-%EC%9C%84%ED%95%9C-T-test-Chi-squared-test
# T-test는 표본집단의 평균을 비교할 때 선택하는 방법
# todo 평균이 비슷하면, pvalue값이 높아지는 것은 알겠는데, 신뢰도가 허용하는 오차범위를 잘 모르겠음. 평균값의 오차 범위가 5%라는 얘기도 아닌 것 같고..

# 데이터셋 불러오기
df = sns.load_dataset("penguins")
df = df.dropna()

# 데이터 프레임 column명 수정
df = df.rename(columns={"species":"species", "island":"island", "bill_length_mm":"bill_length", "bill_depth_mm":"bill_depth",
                        "flipper_length_mm":"flipper_length", "body_mass_g":"body_mass", "sex":"sex"})
#%% one sample T-test

# 신뢰도 95%의 가설을 찾으려면, p-value가 0.05보다 크면, 귀무가설 성립
# 표본 집단의 평균과 추측값을 비교할 때 사용

adelie = df[df["species"] == "Adelie"]["body_mass"]
adelie_mean = adelie.mean()

#귀무가설: Adelie 펭귄의 평균 몸무게는 8kg일 것이다.
#대립가설: Adelie 펭귄의 평균 몸무게는 8kg이 아닐 것이다.
#신뢰도: 95%
result_8000 = stats.ttest_1samp(adelie, 8000) # 단위: g
# one sample T-test 시행 결과, p-value가 0.05보다 작기 때문에 귀무가설을 기각하고 대립가설을 채택한다. 따라서 Adelie 펭귄의 평균 몸무게는 8kg이 아니다.


#귀무가설: Adelie 펭귄의 평균 몸무게는 3.72kg일 것이다.
#대립가설: Adelie 펭귄의 평균 몸무게는 3.72kg이 아닐 것이다.
#신뢰도: 95%
result_3720 = stats.ttest_1samp(adelie, 3850)
# one sample T-test 시행 결과, p-value가 0.05보다 크기 때문에 귀무가설을 기각할 수 없다. 따라서 Adelie 펭귄의 평균 몸무게는 3.72kg이다.


#%% two sample T-test

adelie_bill_depth_mean = adelie.mean()

# 귀무가설: Adelie 펭귄의 평균 부리 깊이와 Gentoo 펭귄의 평균 부리 깊이는 같다.
# 대립가설: Adelie 펭귄의 평균 부리 깊이와 Gentoo 펭귄의 평균 부리 깊이는 같지 않다.
# 신뢰도: 95%
adelie = df[df["species"] == "Adelie"]["bill_depth"]
gentoo = df[df["species"] == "Gentoo"]["bill_depth"]
result_adelie_gentoo = stats.ttest_ind(adelie, gentoo)
gentoo_bill_depth_mean = gentoo.mean()
# two sample T-test 시행 결과, p-value가 0.05보다 작기 때문에 귀무가설을 기각하고 대립가설을 채택한다. 따라서 Adelie 펭귄의 평균 부리 깊이와 Gentoo 펭귄의 평균 부리 깊이는 같지 않다.


# 귀무가설: Adelie 펭귄의 평균 부리 깊이와 Chinstrap 펭귄의 평균 부리 깊이는 같다.
# 대립가설: Adelie 펭귄의 평균 부리 깊이와 Chinstrap 펭귄의 평균 부리 깊이는 같지 않다.
# 신뢰도: 95%
adelie = df[df["species"] == "Adelie"]["bill_depth"]
chinstrap = df[df["species"] == "Chinstrap"]["bill_depth"]
result_adelie_chinstrap = stats.ttest_ind(adelie, chinstrap)
chinstrap_bill_depth_mean = chinstrap.mean()
# two sample T-test 시행 결과, p-value가 0.05보다 크기 때문에 귀무가설을 기각할 수 없다. 따라서 Adelie 펭귄의 평균 부리 깊이와 Chinstrap 펭귄의 평균 부리 깊이는 같다.