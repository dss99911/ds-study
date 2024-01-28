# %% LinearRegression
import numpy as np
from matplotlib import pyplot as plt
from pyspark.sql.functions import spark_partition_id
from sklearn.compose import TransformedTargetRegressor
from sklearn.datasets import make_regression, make_classification
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, median_absolute_error
import pandas as pd
#%%


clf = LinearRegression()
X_train = [[1, 2, 3],  # 2 samples, 3 features
           [11, 12, 13]]
y_train = [0.0, 1.0]  # classes of each sample
clf.fit(X_train, y_train)
y_train_predict = clf.predict(X_train)

X_test = [[4, 5, 6], [14, 15, 16]]
y_test = clf.predict(X_test)

#%% Logistic Regression
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
X_train = [[1, 2, 3],  # 2 samples, 3 features
           [11, 12, 13]]
y_train = [0.0, 1.0]  # classes of each sample
clf.fit(X_train, y_train)
y_train_predict = clf.predict(X_train)

X_test = [[4, 5, 6], [14, 15, 16]]
y_test = clf.predict(X_test)

#%% Random Forest
from sklearn.ensemble import RandomForestRegressor

clf = RandomForestRegressor(random_state=0)
X_train = [[1, 2, 3],  # 2 samples, 3 features
           [11, 12, 13]]
y_train = [0.0, 1.0]  # classes of each sample
clf.fit(X_train, y_train)
y_train_predict = clf.predict(X_train)
X_test = [[4, 5, 6], [14, 15, 16]]
y_test = clf.predict(X_test)

#%% metrics


actual_predict = [
    (1, 10),
    (1000, 10000),
    (1, 2),
    (5, 10),
    (500, 1000),
    (9.99, 10),
    (999, 1000),
    (9990, 10000)
]

for a, p in actual_predict:
    print("msle", a, p, mean_squared_error([a], [p]))

for a, p in actual_predict:
    print("r2", a, p, r2_score([a, a* 1.1, a* 0.9], [p, p*1.1, p* 0.9]))

#%%

X, y = make_regression(n_samples=10000, noise=100, random_state=0)
y = np.expm1((y + abs(y.min())) / 200)
y_trans = np.log1p(y)
a = y.min()
#%%
f, (ax0, ax1) = plt.subplots(1, 2)

ax0.hist(y, bins=100, density=True)
ax0.set_xlim([-2000, 2000])
ax0.set_ylabel("Probability")
ax0.set_xlabel("Target")
ax0.set_title("Target distribution")

ax1.hist(y_trans, bins=100, density=True)
ax1.set_ylabel("Probability")
ax1.set_xlabel("Target")
ax1.set_title("Transformed target distribution")

f.suptitle("Synthetic data", y=0.06, x=0.53)
f.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
plt.show()
#%%
f, (ax0, ax1) = plt.subplots(1, 2, sharey=True)
# Use linear model
regr = RidgeCV()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)
# Plot results
ax0.scatter(y_test, y_pred)
ax0.plot([-2000, 2000], [-2000, 2000], "--k")
ax0.set_ylabel("Target predicted")
ax0.set_xlabel("True Target")
ax0.set_title("Ridge regression \n without target transformation")
ax0.text(
    100,
    1750,
    r"$R^2$=%.2f, MAE=%.2f"
    % (r2_score(y_test, y_pred), median_absolute_error(y_test, y_pred)),
    )
ax0.set_xlim([-2000, 2000])
ax0.set_ylim([-2000, 2000])
# Transform targets and use same linear model
regr_trans = TransformedTargetRegressor(
    regressor=RidgeCV(), func=np.log1p, inverse_func=np.expm1
)

regr_trans.fit(X_train, y_train)
y_pred = regr_trans.predict(X_test)

ax1.scatter(y_test, y_pred)
ax1.plot([0, 2000], [0, 2000], "--k")
ax1.set_ylabel("Target predicted")
ax1.set_xlabel("True Target")
ax1.set_title("Ridge regression \n with target transformation")
ax1.text(
    100,
    1750,
    r"$R^2$=%.2f, MAE=%.2f"
    % (r2_score(y_test, y_pred), median_absolute_error(y_test, y_pred)),
    )
ax1.set_xlim([-2000, 2000])
ax1.set_ylim([-2000, 2000])

f.suptitle("Synthetic data", y=0.035)
f.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
plt.show()

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

f, (ax0, ax1) = plt.subplots(1, 2)

ax0.hist(y, bins=100, density=True)
ax0.set_ylabel("Probability")
ax0.set_xlabel("Target")
ax0.text(s="Target distribution", x=1.2e5, y=9.8e-6, fontsize=12)
ax0.ticklabel_format(axis="both", style="sci", scilimits=(0, 0))

ax1.hist(y_trans, bins=100, density=True)
ax1.set_ylabel("Probability")
ax1.set_xlabel("Target")
ax1.text(s="Transformed target distribution", x=-6.8, y=0.479, fontsize=12)

f.suptitle("Ames housing data: selling price", y=0.04)
f.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
plt.show()
