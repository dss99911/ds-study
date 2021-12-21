from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pipe = make_pipeline(
    StandardScaler(),
    LogisticRegression()
)
X, y = load_iris(return_X_y=True)

# 데이터와 정답셋을 셔플해서, train과 test로 임의로 분리한다.
# 특정 train으로 학습하고, test하면 정상으로 맞추는데, 다른 train으로 학습하면, 못맞추는 경우도 있을 수 있어서, 여러번 섞어서 학습 시키는듯..?
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)

# fit the whole pipeline
pipe.fit(X_train, y_train)

# we can now use it like any other estimator
score = accuracy_score(pipe.predict(X_test), y_test)

#%%