# transformer는 데이터를 다른 데이터로 바꾸는 것(transform)
# estimator는 데이터로 학습을 시킨 후(fit), 다른 데이터로 바꾸는 것(transform)
#   - preprocessing단계에서 feature생성을 위해 사용하는 경우가 있고,
#   - classifier, regression등 ml 모델등 이 있디.
from pyspark.sql import SparkSession
from pyspark.sql.types import *


spark = SparkSession.builder \
    .appName("Spark NLP") \
    .getOrCreate()

schema = StructType([
    StructField('sepal_length', DoubleType(), nullable=False),
    StructField('sepal_width', DoubleType(), nullable=False),
    StructField('petal_length', DoubleType(), nullable=False),
    StructField('petal_width', DoubleType(), nullable=False),
    StructField('class', StringType(), nullable=False)
])

iris = spark.read.csv('./data/iris.data', schema=schema)
iris.createOrReplaceTempView('iris')
#%% SQLTransformer

from pyspark.ml.feature import SQLTransformer

statement = '''
SELECT 
    class, 
    min(sepal_length), avg(sepal_length), max(sepal_length),
    min(sepal_width), avg(sepal_width), max(sepal_width),
    min(petal_length), avg(petal_length), max(petal_length),
    min(petal_width), avg(petal_width), max(petal_width)
FROM iris
GROUP BY class
'''

sql_transformer = SQLTransformer(statement=statement)

df_sql_transformer = sql_transformer.transform(iris).toPandas()

#%% Binarizer
from pyspark.ml.feature import Binarizer

binarizer = Binarizer(
    inputCol='sepal_length',
    outputCol='sepal_length_above_5',
    threshold=5.0
)

binarizer.transform(iris).limit(5).toPandas()

#%% VectorAssembler
# 5.1	3.5	1.4	0.2	 => [5.1, 3.5, 1.4, 0.2]
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=[
        'sepal_length', 'sepal_width',
        'petal_length', 'petal_width'
    ],
    outputCol='features'
)

iris_w_vecs = assembler.transform(iris).persist()
iris_w_vecs.limit(5).toPandas()

#%% MinMaxScaler
# make value from 0 to 1.
# 수치를 바꾸려면, 데이터의 최소값 최대값이 필요하고,
# trained data에 있는 것보다 더 큰 데이터가 serving시에 있는 경우에는 정확한 값이 아니므로 estimator로 분류
# [5.1, 3.5, 1.4, 0.2] => [0.22222222222222213, 0.6249999999999999, 0.06...
from pyspark.ml.feature import MinMaxScaler

scaler = MinMaxScaler(
    inputCol='features',
    outputCol='petal_length_scaled'
)
scaler_model = scaler.fit(iris_w_vecs)
scaler_model.transform(iris_w_vecs).limit(5).toPandas()

#%% StringIndexer, IndexToString
from pyspark.ml.feature import StringIndexer, IndexToString

indexer = StringIndexer(inputCol='class', outputCol='class_ix')
indexer_model = indexer.fit(iris_w_vecs)

index2string = IndexToString(
    inputCol=indexer_model.getOrDefault('outputCol'),
    outputCol='pred_class',
    labels=indexer_model.labels
)

iris_indexed = indexer_model.transform(iris_w_vecs)

#%%
from pyspark.ml.classification import DecisionTreeClassifier

dt_clfr = DecisionTreeClassifier(
    featuresCol='features',
    labelCol='class_ix',
    maxDepth=5,
    impurity='gini',
    seed=123
)

dt_clfr_model = dt_clfr.fit(iris_indexed)
iris_w_pred = dt_clfr_model.transform(iris_indexed)
iris_w_pred.limit(5).toPandas()
iris_w_pred_class = index2string.transform(iris_w_pred)
iris_w_pred_class.limit(5).toPandas()

#%% MulticlassClassificationEvaluator
# 모델 평가하기. 0~1 사이의 정확도를 리턴함.
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(
    labelCol='class_ix',
    metricName='accuracy'
)

evaluator.evaluate(iris_w_pred_class)

#%% Pipeline

from pyspark.ml import Pipeline

pipeline = Pipeline(stages=[
    assembler,
    indexer,
    dt_clfr,
    index2string
])

pipeline_model = pipeline.fit(iris)
pipeline_model.transform(iris).limit(5).toPandas()

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
#%% write pipeline model

pipeline_model.write().overwrite().save('pipeline.model')