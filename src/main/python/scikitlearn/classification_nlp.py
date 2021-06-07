# %%
# https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

twenty_train = fetch_20newsgroups(subset='train', shuffle=True)

text_clf = Pipeline([('vect', CountVectorizer(stop_words='english', ngram_range=(1,2))),
                     ('tfidf', TfidfTransformer(use_idf=True)),
                     ('clf', MultinomialNB(alpha=0.01)),
                     # ('clf',
                     #  SGDClassifier(loss='hinge', penalty='l2', alpha=0.001, n_iter_no_change=5, random_state=42)),
                     ])

text_clf = text_clf.fit(twenty_train.data, twenty_train.target)

twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
predicted = text_clf.predict(twenty_test.data)
score = np.mean(predicted == twenty_test.target)

# 아래의 파라미터중에 어떤게 효과적인지 찾는다.
def find_best_parameter():
    parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
                  'tfidf__use_idf': (True, False),
                  'clf__alpha': (1e-2, 1e-3),
                  }

    gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(twenty_train.data, twenty_train.target)
    return gs_clf.best_score_, gs_clf.best_params_

# best_score, best_params = find_best_parameter()

# todo best score는 91% 나오는데, 왜, best_params를 직접 설정하면, 83%가 나오지?