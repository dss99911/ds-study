from sklearn.datasets import load_iris
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
#%%

# hue로 그룹을 만들어서,
# 각 column들의 그룹별 도수 분포도(histogram).(그룹 별, 각 column이 일정한 범이안에 위치하는지 확인(
# 두 column을 결합해서, 산점도(scatter)를 보여준다.(classifier가 분류를 할 수 있을지, 각 두 컬럼을 비교하기)
sns.pairplot(iris_df, hue="species", height = 2, palette = 'colorblind')
plt.show()
