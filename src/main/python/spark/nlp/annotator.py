
from sparknlp import DocumentAssembler, Finisher
import sparknlp
from pyspark.sql.types import *

# %%

spark = sparknlp.start()
# RDD containing filepath-text pairs
texts = spark.sparkContext.wholeTextFiles("data/mini_newsgroups/*")

schema = StructType([
    StructField('path', StringType()),
    StructField('text', StringType()),
])

texts = spark.createDataFrame(texts, schema=schema)

# %% DocumentAssembler
# document 라는 annotatorType으로 변환. spark NLP에서는 모든 데이터는 annotation에서 다른 annotation으로 변환 되는듯.
document_assembler: DocumentAssembler = DocumentAssembler() \
    .setInputCol('text') \
    .setOutputCol('document') \
    .setIdCol('path')

docs = document_assembler.transform(texts)
docs.first()['document'][0].asDict()
# %% SentenceDetector : change document to senteense

from sparknlp.annotator import SentenceDetector, Normalizer

sent_detector = SentenceDetector() \
    .setInputCols('document') \
    .setOutputCol('sentences')

sentences = sent_detector.transform(docs)
sentences.first()['sentences'][0].asDict()

#%% Tokenizer
from sparknlp.annotator import Tokenizer
# The Spark NLP Tokenizer is a little more sophisticated than just a regular expression-based tokenizer
#  - regex tokenizer : from nltk.tokenize import RegexpTokenizer
tokenizer = Tokenizer() \
    .setInputCols('sentences') \
    .setOutputCol('tokens') \
    .fit(sentences)

tokens = tokenizer.transform(sentences)

tokens.limit(5).toPandas().to_dict()

#%% Lemmatizer
from sparknlp.annotator import Lemmatizer
# 특정 단어의 표제어(are의 경우 be) 찾기. 각 사용케이스에 맞춰서, dictionary를 customizing할 수 있음
lemmatizer = Lemmatizer() \
    .setInputCols("tokens") \
    .setOutputCol("lemma") \
    .setDictionary('data/en_lemmas.txt', '\t', ',') \
    .fit(tokens)

lemmas = lemmatizer.transform(tokens)
lemmas.limit(5).toPandas()

#%% normalizer
# change to lower case, clean up by regex
normalizer = Normalizer() \
    .setInputCols(["token"]) \
    .setOutputCol("normalized") \
    .setLowercase(True) \
    .setCleanupPatterns(["""[^\w\d\s]"""]) # remove punctuations (keep alphanumeric chars)
# if we don't set CleanupPatterns, it will only keep alphabet letters ([^A-Za-z])

#%% PerceptronModel

from sparknlp.annotator import PerceptronModel

pos_tagger = PerceptronModel.pretrained() \
    .setInputCols("tokens", "sentences") \
    .setOutputCol("pos")

postags = pos_tagger.transform(tokens)
postags.limit(5).toPandas()

#%% annotator pipieline 결합 활용

from pyspark.ml import Pipeline
finisher = Finisher() \
    .setInputCols('tokens', 'lemma') \
    .setOutputCols('tokens', 'lemmata') \
    .setCleanAnnotations(True) \
    .setOutputAsArray(True)

custom_pipeline = Pipeline(stages=[
    document_assembler,
    sent_detector,
    tokenizer,
    lemmatizer,
    finisher
]).fit(texts)

lemmata = custom_pipeline.transform(texts).first()["lemmata"]

#%% stopwords.
# 전처리 끝난 후, stopwords를 마지막에 함으로써, stopwords dictionary에는 표제어만 추가하면 되게 하고 있음
from pyspark.ml.feature import StopWordsRemover

# is, from, of, i, me, my등의 리스트
stopwords = StopWordsRemover.loadDefaultStopWords('english')

#pipeline은 다른 pipeline을 가질 수 있음
larger_pipeline = Pipeline(stages=[
    custom_pipeline,
    StopWordsRemover(
        inputCol='lemmata',
        outputCol='terms',
        stopWords=stopwords)
]).fit(texts)

terms = larger_pipeline.transform(texts).first()["terms"]

#%% LightPipeline
# DataFrame을 transform하는 것이 아닌 텍스트를 annotate 할 수 있음
from sparknlp.base import LightPipeline
light = LightPipeline(larger_pipeline)
light.annotate("We are very happy about Spark NLP")