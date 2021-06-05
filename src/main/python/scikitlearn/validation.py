from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_validate, train_test_split

X, y = make_regression(n_samples=1000, random_state=0)
lr = LinearRegression()

# train 데이터와 test데이터를 임의로 분리한다.
# 학습시킨 모델의 성능 평가를 위해서, test데이터를 별도로 빼서, 테스트를 돌려본다.
# random_state : 변하지 않는 랜덤 값을 사용하고 싶을 때 입력.
# test_size : train할 데이터와 test할 데이터 비율을 나눌 때 사용.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

lr.fit(X_train, y_train)

score = lr.score(X_test, y_test)

#%% cross validation
# https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
# 한번만 validation 할 경우, train과 test가 우연히 잘 맞아 떨어져서 좋은 점수가 나올 수도 있다.
# 여러번 검증하기

result = cross_validate(lr, X, y)  # defaults to 5-fold CV
result['test_score']  # r_squared score is high because dataset is easy

#%%