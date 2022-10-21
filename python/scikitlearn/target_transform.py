# https://scikit-learn.org/stable/auto_examples/compose/plot_transformed_target.html

# rmse + log1p를 적용하는 경우
#  - 레이블이 양수로만 되어있는 경우,
#  - 학습시, 모델은 레이블이 양수만 존재하는지 알지 못한다.
#  - 값을 음수로도 골고루 분산 시켜주어서, 학습을 돕는 듯
#  - y.median() == np.expm1(np.log1p(y).median()) 일치한다고 한다.
#  - log1p를 취할 경우, 모델 예측값의 분포도가 y_log1p와 비슷해지는데, 예측치의 평균도 y_log1p의 평균과 비슷해질 것이고,
#       - 예측값을 expm1을 하게 됐을 때의 평균은, np.expm1(y_log1p_mean)의 평균과 비슷해지므로,
#       - rmse(y, np.expm1(y_log1p_mean)) 와 rmse(y, y.mean()) 의 차이가 작다면, log1p를 적용함으로써 label이 다른 쪽으로 편향될 가능성은 낮아서, 적용하기 좋다고 판단할 수 있다는 듯
#       - rmse_mean = mean_squared_error(y_original, len(y_original) * [y_original.mean()], squared=False)
#       - rmse_mean_log1p = mean_squared_error(y_original, len(y_original) * np.expm1( y_log1p.mean()), squared=False)
#  - rmse_pred = mean_squared_error(y_original, np.expm1(y_log1p_pred), squared=False)

import numpy as np
from matplotlib import pyplot as plt
from pyspark.sql.functions import spark_partition_id
from sklearn.compose import TransformedTargetRegressor
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, median_absolute_error
from matplot.ml_matplot_functions import show_target_distribution, show_prediction_scatter

#%%
X, y = make_regression(n_samples=10000, noise=100, random_state=0)
y = np.expm1((y + abs(y.min())) / 200)
y_trans = np.log1p(y)

#%%

show_target_distribution(y)
show_target_distribution(y_trans)
#%%
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

f, (ax0, ax1) = plt.subplots(1, 2, sharey=True)
# Use linear model
regr = RidgeCV()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)

show_prediction_scatter(y_test, y_pred)

regr_trans = TransformedTargetRegressor(
    regressor=RidgeCV(), func=np.log1p, inverse_func=np.expm1
)

regr_trans.fit(X_train, y_train)
y_pred_trans = regr_trans.predict(X_test)
show_prediction_scatter(y_test, y_pred_trans)


#%%

from sklearn.datasets import fetch_openml
from sklearn.preprocessing import QuantileTransformer, quantile_transform

ames = fetch_openml(name="house_prices", as_frame=True)
# Keep only numeric columns
X = ames.data.select_dtypes(np.number)
# Remove columns with NaN or Inf values
X = X.drop(columns=["LotFrontage", "GarageYrBlt", "MasVnrArea"])
y = ames.target
y_trans = quantile_transform(
    y.to_frame(), n_quantiles=900, output_distribution="normal", copy=True
).squeeze()

show_target_distribution(y)
show_target_distribution(y_trans)

