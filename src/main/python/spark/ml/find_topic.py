from spark.nlp.annotator import *
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.ml.clustering import LDA

#%% CountVectorizer (Term Frequency)
# bag-of-words 단어가방. 단어별로 가방이 있고, 가방은 단어의 수를 의미
# 단어를 숫자로 변환. 총 단어 수 및, 각 단어 별, 갯수 리턴
tf = CountVectorizer(inputCol='terms', outputCol='tf')

# fit이후, tf_model.vocabulary[ix] 로 vector와 word맵핑 확인 가능

#%% IDF(Inverse Document Frequency)는
# DF : 문서의 빈도(단어가 얼마나 많은 문서에 나오는가)에 따라 단어의 가중치를 줌
# IDF : 문서의 빈도가 낮은 경우에 가중치가 높음
# tf에서의 갯수 값을 가중치 값으로 변경(fit할때, 각 단어별 IDF값이 정해지고, transfer로 특정 문서의 tfidf를 구할 때, tf * idf를 함)
# IDF사용 이유 : topic을 찾을 때, 문서 빈도가 낮은 단어가 해당 문서의 topic과 관련있을 가능성이 높으므로 idf를 사용.
idf = IDF(inputCol='tf', outputCol='tfidf')

#%% LDA(Latent Dirichlet Allocation)
# 10개의 topic을 생성하고, 각 문서가 토픽인지에 대한 확률을 리턴함
lda = LDA(k=10, seed=123, featuresCol='tfidf')

#%% lda pipeline
model = Pipeline(stages=[
    larger_pipeline,
    tf,
    idf,
    lda
]).fit(texts)

#%%
result = model.transform(example_alt_atheism)
result1 = result.first().asDict()
tf_model = model.stages[-3]
lda_model = model.stages[-1]

#%% 토픽 확인하고, 각 토픽으로 선택되는 가중치 확인
topics = lda_model.describeTopics().collect()
for k, topic in enumerate(topics):
    print('Topic', k)
    for ix, wt in zip(topic['termIndices'], topic['termWeights']):
        print(ix, tf_model.vocabulary[ix], wt)
    print('#' * 50)

#%% 어휘 빈도 구하기, n-gram, idf

from spark.ml.util import *
from matplot.util import *

from pyspark.ml.feature import NGram
# https://books.google.com/ngrams
# - 책에 특정 구문이 나오는 빈도를 연도별로 보여줌
bigrams = NGram() \
    .setN(2) \
    .setInputCol("normalized") \
    .setOutputCol("bigrams")
trigrams = NGram() \
    .setN(3) \
    .setInputCol("normalized") \
    .setOutputCol("trigrams")

model = Pipeline(stages=[
    larger_pipeline,
    tf,
    IDF(inputCol='tf', outputCol='tfidf'),
    bigrams,
    trigrams,
    CountVectorizer(inputCol='bigrams', outputCol='bigrams_tf'),
    CountVectorizer(inputCol='trigrams', outputCol='trigrams_tf')
]).fit(example_sci_space)

result = model.transform(example_sci_space)
#%%
vocabulary = model.stages[1].vocabulary
vocabulary2 = model.stages[-2].vocabulary
vocabulary3 = model.stages[-1].vocabulary
#%%
from spark.ml.util import *
# 파일이 달라서인지, collect_counter에서 lambda에 있는 vocabulary를 인식하지 못함. spark.ml.util 의 셀을 실행하고 하면 됨.
word_counts = collect_counter(result, "tf", lambda i: vocabulary[i])
word_countsi = collect_counter(result, "tfidf", lambda i: vocabulary[i])
word_counts2 = collect_counter(result, "bigrams_tf", lambda i: vocabulary2[i])
word_counts3 = collect_counter(result, "trigrams_tf", lambda i: vocabulary3[i])

show_counter_bar(word_counts, 20, "unigram")
show_counter_bar(word_countsi, 20, "tfidf")
show_counter_bar(word_counts2, 20, "bigrams")
show_counter_bar(word_counts3, 20, "trigrams")

show_word_cloud(word_counts, "unigram")
show_word_cloud(word_countsi, "tfidf")
show_word_cloud(word_counts2, "bigrams")
show_word_cloud(word_counts3, "trigrams")
