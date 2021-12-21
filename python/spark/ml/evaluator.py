from spark.ml.transformer_estimator import *

#%% split data for evaluate
train, test = texts.randomSplit([0.8, 0.2], seed=123)

#%% MulticlassClassificationEvaluator
# 모델 평가하기. 0~1 사이의 정확도를 리턴함.
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(
    labelCol='class_ix',
    metricName='accuracy'  # default is f1
)

evaluator.evaluate(iris_w_pred_class)

evaluator = MulticlassClassificationEvaluator(metricName='f1')
print('f1', evaluator.evaluate(iris_w_pred_class))
# f1 score가 test에서 많이 낮으면 overfitting된 걸 의미

#%% cross validation

from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# performance tuning을 위한 validate할 parameter들을 지정
param_grid = ParamGridBuilder(). \
    addGrid(dt_clfr.maxDepth, [5, 6]). \
    build()
cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=param_grid,
    evaluator=evaluator,
    numFolds=3,
    seed=123
)

cv_model = cv.fit(iris)
avgMetrics = cv_model.avgMetrics