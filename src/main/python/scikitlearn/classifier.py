from sklearn.ensemble import RandomForestClassifier

# X, y(label) 정답셋을 학습 시키면, X를 넣었을 때, y를 리턴한다.

#%% RandomeForest


clf = RandomForestClassifier(random_state=0)
X_train = [[1, 2, 3],  # 2 samples, 3 features
           [11, 12, 13]]
y_train = [0, 1]  # classes of each sample
clf.fit(X_train, y_train)
y_train_predict = clf.predict(X_train)
X_test = [[4, 5, 6], [14, 15, 16]]
y_test = clf.predict(X_test)

#%% Decision Tree
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=10)
X_train = [[1, 2, 3],  # 2 samples, 3 features
           [11, 12, 13]]
y_train = [0, 1]  # classes of each sample
clf.fit(X_train, y_train)
y_train_predict = clf.predict(X_train)

X_test = [[4, 5, 6], [14, 15, 16]]
y_test = clf.predict(X_test)