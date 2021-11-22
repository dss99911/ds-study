from spark.nlp.annotator import *
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.ml.clustering import LDA

# 단어를 숫자로 변환. 총 단어 수 및, 각 단어 별, 갯수 리턴
tf = CountVectorizer(inputCol='terms', outputCol='tf')

#TF-IDF(Term Frequency-Inverse Document Frequency)는
# 단어의 빈도와 역 문서 빈도(문서의 빈도에 특정 식을 취함)를 사용하여
# 문서 빈도(단어가 얼마나 많은 문서에 나오는가)에 따라 단어들의 가중치를 달리 하기
# tf에서의 갯수 값을 가중치 값으로 변경
idf = IDF(inputCol='tf', outputCol='tfidf')

# 10개의 topic을 생성하고, 각 문서가 토픽인지에 대한 확률을 리턴함
lda = LDA(k=10, seed=123, featuresCol='tfidf')

pipeline = Pipeline(stages=[
    larger_pipeline,
    tf,
    idf,
    lda
])

model = pipeline.fit(texts)
result = model.transform(texts)
result1 = result.first().asDict()
tf_model = model.stages[-3]
lda_model = model.stages[-1]

#토픽 확인하고, 각 토픽으로 선택되는 가중치 확인
topics = lda_model.describeTopics().collect()
for k, topic in enumerate(topics):
    print('Topic', k)
    for ix, wt in zip(topic['termIndices'], topic['termWeights']):
        print(ix, tf_model.vocabulary[ix], wt)
    print('#' * 50)

#%%