from sklearn.datasets import load_iris
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
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
#%% 도수분포, 산점도 보여주기

# hue로 그룹을 만들어서,
# 각 column들의 그룹별 도수 분포도(histogram).(그룹 별, 각 column이 일정한 범이안에 위치하는지 확인(
# 두 column을 결합해서, 산점도(scatter)를 보여준다.(classifier가 분류를 할 수 있을지, 각 두 컬럼을 비교하기)
sns.pairplot(iris_df, hue="species", height = 2, palette = 'colorblind')
plt.show()

#%% 상관 계수, heatmap으로 보여주기
fig, ax = plt.subplots(figsize=(5, 4))
ax = sns.heatmap(iris_df.corr(), vmin=-1, vmax=1,
                 cmap=sns.diverging_palette(20, 220, as_cmap=True),
                 ax=ax)

plt.tight_layout()
plt.show()


#%% 상관계수 타원형 보여주기

from matplotlib.collections import EllipseCollection
from matplotlib.colors import Normalize

def plot_corr_ellipses(data, figsize=None, **kwargs):
    ''' https://stackoverflow.com/a/34558488 '''
    M = np.array(data)
    if not M.ndim == 2:
        raise ValueError('data must be a 2D array')
    fig, ax = plt.subplots(1, 1, figsize=figsize, subplot_kw={'aspect':'equal'})
    ax.set_xlim(-0.5, M.shape[1] - 0.5)
    ax.set_ylim(-0.5, M.shape[0] - 0.5)
    ax.invert_yaxis()

    # xy locations of each ellipse center
    xy = np.indices(M.shape)[::-1].reshape(2, -1).T

    # set the relative sizes of the major/minor axes according to the strength of
    # the positive/negative correlation
    w = np.ones_like(M).ravel() + 0.01
    h = 1 - np.abs(M).ravel() - 0.01
    a = 45 * np.sign(M).ravel()

    ec = EllipseCollection(widths=w, heights=h, angles=a, units='x', offsets=xy,
                           norm=Normalize(vmin=-1, vmax=1),
                           transOffset=ax.transData, array=M.ravel(), **kwargs)
    ax.add_collection(ec)

    # if data is a DataFrame, use the row/column names as tick labels
    if isinstance(data, pd.DataFrame):
        ax.set_xticks(np.arange(M.shape[1]))
        ax.set_xticklabels(data.columns, rotation=90)
        ax.set_yticks(np.arange(M.shape[0]))
        ax.set_yticklabels(data.index)

    return ec

m = plot_corr_ellipses(iris_df.corr(), figsize=(5, 4), cmap='bwr_r')
cb = fig.colorbar(m)
cb.set_label('Correlation coefficient')

plt.tight_layout()
plt.show()