# TODO 결과 값과 입력 값 사이에, 어떤 상관 관계가 있는지.확인하기
import numpy as np
from sklearn.linear_model import LinearRegression
clf = LinearRegression()
X_train = [[1],  # 2 samples, 3 features
           [2]]
y_train = [2, 4]  # classes of each sample
clf.fit(X_train, y_train)
y_train_predict = clf.predict(X_train)

X_test = [[4], [5]]
y_test = clf.predict(X_test)

coer = clf.coef_  # Weight 기울기
intercept = clf.intercept_  # bias. y절편
