# %% LinearRegression
from sklearn.linear_model import LinearRegression
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
