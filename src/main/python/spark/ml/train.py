from spark.ml.util import *
from spark.nlp.annotator import *

# %% train
texts = texts.withColumn('newsgroup', expr('reverse(split(path, "/"))[1]'))
texts = larger_pipeline_load.transform(texts)  # 하나의 pipeline에 nlp와 ml 파이프라인 둘다 추가하면, CrossValidator를 쓸 때, 에러남. https://github.com/JohnSnowLabs/spark-nlp/issues/1158
train, test = texts.randomSplit([0.8, 0.2], seed=123)

count_vectorizer = CountVectorizer(inputCol='terms',
                                   outputCol='tf', minDF=10)
idf = IDF(inputCol='tf', outputCol='tfidf', minDocFreq=10)

label_indexer = StringIndexer(inputCol='newsgroup', outputCol='label').fit(texts)
naive_bayes = NaiveBayes(featuresCol='tfidf')
prediction_deindexer = IndexToString(inputCol='prediction', outputCol='pred_newsgroup',
                                     labels=label_indexer.labels)

pipeline = Pipeline(stages=[
    count_vectorizer,
    idf,
    label_indexer,
    naive_bayes,
    prediction_deindexer
])

model = pipeline.fit(train)
# %% evaluate
train_predicted = model.transform(train)
test_predicted = model.transform(test)

evaluator = MulticlassClassificationEvaluator(metricName='f1')

print('f1', evaluator.evaluate(train_predicted))
print('f1', evaluator.evaluate(test_predicted))
# f1 score가 test에서 많이 낮으면 overfitting된 걸 의미

evaluator = MulticlassClassificationEvaluator(
    labelCol='label',  # label col이 'label'이 아닌 경우
    metricName='accuracy'  # default is f1
)

# %% cross validation
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# performance tuning을 위한 validate할 parameter들을 지정
param_grid = ParamGridBuilder(). \
    addGrid(idf.minDocFreq, [10, 20]). \
    build()
cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=param_grid,
    evaluator=evaluator,
    numFolds=3,
    seed=123
)

cv_model = cv.fit(texts)
avgMetrics = cv_model.avgMetrics
