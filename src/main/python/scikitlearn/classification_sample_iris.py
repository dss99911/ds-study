# %%
# https://dschloe.github.io/python/python_edu/04_machinelearning/chapter_4_4_classification_iris_example/
# 분석 후, linear model적용하는 것까지 설명

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# %% 분석
def get_pandas_df():
    iris = load_iris()
    iris_data = iris.data
    iris_label = iris.target
    iris_target_names = iris.target_names
    iris_df = pd.DataFrame(data=iris_data, columns=iris.feature_names)
    iris_df['label'] = iris.target
    replace_fct = {0: 'setosa', 1: 'versicolor', 2: "virginica"}
    iris_df.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
    iris_df['species'] = iris_df['species'].map(replace_fct)

    return iris_df


iris_df = get_pandas_df()

n_bins = 10
fig, axs = plt.subplots(2, 2)  # 그래프를 그리기 위해 일종의 레이아웃을 작성한다.
axs[0, 0].hist(iris_df['sepal_length'], bins=n_bins)
axs[0, 0].set_title('Sepal Length')
axs[0, 1].hist(iris_df['sepal_width'], bins=n_bins)
axs[0, 1].set_title('Sepal Width')
axs[1, 0].hist(iris_df['petal_width'], bins=n_bins)
axs[1, 0].set_title('Pepal Width')
axs[1, 1].hist(iris_df['petal_length'], bins=n_bins)
axs[1, 1].set_title('Pepal Length')

fig.tight_layout(pad=1.0)
plt.show()

# %% 도수분포도 및 산점도 확인
import seaborn as sns

# hue로 그룹을 만들어서,
# 각 column들의 그룹별 도수 분포도(histogram).(그룹 별, 각 column이 일정한 범이안에 위치하는지 확인(
# 두 column을 결합해서, 산점도(scatter)를 보여준다.(classifier가 분류를 할 수 있을지, 각 두 컬럼을 비교하기)
sns.pairplot(iris_df, hue="species", height=2, palette='colorblind')
plt.show()

# %% Linear model 적용

# load the iris dataset and split it into train and test sets
X, y = load_iris(return_X_y=True)

# train 데이터와 test데이터를 임의로 분리한다.
# 학습시킨 모델의 성능 평가를 위해서, test데이터를 별도로 빼서, 테스트를 돌려본다.
# random_state : 변하지 않는 랜덤 값을 사용하고 싶을 때 입력.
# test_size : train할 데이터와 test할 데이터 비율을 나눌 때 사용.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# create a pipeline object
pipe = make_pipeline(
    StandardScaler(),
    LogisticRegression()
)


# fit the whole pipeline
pipe.fit(X_train, y_train)

# we can now use it like any other estimator
score = accuracy_score(pipe.predict(X_test), y_test)

#%% cross validation
# 한번만 validation 할 경우, train과 test가 우연히 잘 맞아 떨어져서 좋은 점수가 나올 수도 있다.
# 여러번 검증하기
validation_result = cross_validate(pipe, X,y)


#%%
from sklearn.metrics import plot_confusion_matrix

# 정답과, 예측의 차이를 보여준다.
# 어떤 부분에서 오차가 심한지 확인하여, 튜닝할 위치를 보여준다.

disp = plot_confusion_matrix(pipe,
                             X_test, y_test,
                             display_labels=['setosa', 'versicolor', 'virginica'],#정답셋 레이블 명, label 0,1,2에 대한,이름
                             cmap=plt.cm.Reds,
                             normalize=None)
disp.ax_.set_title('Confusion Matrix')
plt.show()