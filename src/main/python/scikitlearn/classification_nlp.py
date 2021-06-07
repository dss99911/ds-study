from sklearn.datasets import fetch_20newsgroups


twenty_train = fetch_20newsgroups(subset='train', shuffle=True)


#%%

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
shape = X_train_counts.shape