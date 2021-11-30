from sparknlp import DocumentAssembler, Finisher
from spark.nlp.example import *

# %% DocumentAssembler
# document 라는 annotatorType으로 변환. spark NLP에서는 모든 데이터는 annotation에서 다른 annotation으로 변환 되는듯.
document_assembler: DocumentAssembler = DocumentAssembler() \
    .setInputCol('text') \
    .setOutputCol('document')

docs = document_assembler.transform(texts)
docs.first()['document'][0].asDict()
# %% SentenceDetector : change document to senteense

from sparknlp.annotator import SentenceDetector, Normalizer, Stemmer

sent_detector = SentenceDetector() \
    .setInputCols('document') \
    .setOutputCol('sentences')

sentences = sent_detector.transform(docs)
sentences.first()['sentences'][0].asDict()

#%% Tokenizer
from sparknlp.annotator import Tokenizer
from pyspark.ml.feature import RegexTokenizer
# The Spark NLP Tokenizer is a little more sophisticated than just a regular expression-based tokenizer

tokenizer: Tokenizer = Tokenizer()
# 책과 달리, couldn't 가 분리 되지 않음
# tokenizer = tokenizer.setTargetPattern("\\w+")  # default is "\\S+
# tokenizer = tokenizer.setInfixPatterns(["(.*)"])  # 예비 토큰의 일부만 매칭되도 됨. use 1st group as token if regex matched
# tokenizer = tokenizer.setSplitPattern("'") # if this exists, exclude from tokens
# tokenizer = tokenizer.addException("Robert Knowles")  # make this one token. other option : setExceptins(list)
# tokenizer = tokenizer.setPrefixPattern("\\A\\S(\\S+)")  # 예비 토큰에서 매칭되는 패턴 그룹 찾기
tokenizer = tokenizer.setInputCols('sentences')
tokenizer = tokenizer.setOutputCol('tokens')

tokens = tokenizer.fit(sentences).transform(sentences)
token_dict = tokens.limit(5).toPandas().to_dict()

# Spark ML's RegexTokenizer
# regex \b is boundary. start and end of alpha-numeric
ws_tokenizer = RegexTokenizer() \
    .setInputCol('text') \
    .setOutputCol('ws_tokens') \
    .setPattern('\\s+|\\b') \
    .setGaps(True) \
    .setToLowercase(False)

#%% Spelling Correction
# - SymmetricDelete
#   - 올바른 단어 사전에서 검색
# - NorvigSweeting
#   - 올바른 단어 사전 있지만, 가장 가능성있는 단어를 제안함.
# 둘다, 앞뒤 문맥을 파악해서 교정하는 건 아니고, 단어 자체만 가지고서 판단함
# - Hunspell
#   - 맞춤법 검사 및 형태학적 분석에 광범위하게 쓰이는 라이브러리
#   - hunspell.github.io
from sparknlp.annotator import NorvigSweetingModel
from sparknlp.annotator import SymmetricDeleteModel

norvig = NorvigSweetingModel.pretrained() \
    .setInputCols('tokens') \
    .setOutputCol('norvig')

#%% Stemmer 어간 추출
# - 딕셔너리가 없다. 알고리즘 기반
# - 알 수 없는 단어가 많이 있는 경우
# - 의미에 따른 단어의 결합의 경우, 어간 추출이 거의 불가능
from sparknlp.annotator import Stemmer

stemmer: Stemmer = Stemmer()
stemmer = stemmer.setInputCols("tokens")
stemmer = stemmer.setOutputCol("stems")

#%% Lemmatizer 표제어 추출
# - 해시맵 조회라서 빠르다
# - 실제 단어를 반환하므로, 활용이 보다 쉽다
# - 알 수있는 단어가 대부분인 경우 사용.
# - 단어의 형태가 풍부한 경우, 그만큼 큰 사전이 있어야함.
from sparknlp.annotator import Lemmatizer, LemmatizerModel
# 특정 단어의 표제어(are의 경우 be) 찾기. 각 사용케이스에 맞춰서, dictionary를 customizing할 수 있음

lemmatizer: Lemmatizer = LemmatizerModel.pretrained()
lemmatizer = lemmatizer.setInputCols("norvig")
lemmatizer = lemmatizer.setOutputCol("lemma")

lemmatizer_custom = Lemmatizer() \
    .setInputCols("tokens") \
    .setOutputCol("lemma") \
    .setDictionary('data/en_lemmas.txt', '\t', ',')


lemmas = lemmatizer_custom.fit(tokens).transform(tokens)
lemmas.limit(5).toPandas()

#%% normalizer
# change to lower case, clean up by regex
normalizer = Normalizer() \
    .setInputCols("lemma") \
    .setOutputCol("normalized") \
    .setLowercase(True) \
    # .setCleanupPatterns(["""[^\w\d\s]"""]) # remove punctuations (keep alphanumeric chars)
# if we don't set CleanupPatterns, it will only keep alphabet letters ([^A-Za-z])

#%% PerceptronModel 문장의 각 성분 분석

from sparknlp.annotator import PerceptronModel

pos_tagger = PerceptronModel.pretrained() \
    .setInputCols("tokens", "sentences") \
    .setOutputCol("pos")

postags = pos_tagger.transform(tokens)
postags.limit(5).toPandas()

#%% annotator pipieline 결합 활용

from pyspark.ml import Pipeline

stages = [
    document_assembler,
    sent_detector,
    tokenizer,
    norvig,
    stemmer,
    lemmatizer,
    normalizer
]

# 모든 컬럼을 확인하기 위해서 임으로 전부 추가함
outputCols = list(map(lambda s: s.getOrDefault("outputCol"), stages))
finisher = Finisher() \
    .setInputCols(*outputCols) \
    .setOutputCols(*outputCols) \
    .setCleanAnnotations(True) \
    .setOutputAsArray(True)

custom_pipeline = Pipeline(stages= stages + [finisher]).fit(texts)
#%% see the result
result = custom_pipeline.transform(example).first().asDict()

#%% stopwords.
# - 전처리 끝난 후, stopwords를 마지막에 함으로써, stopwords dictionary에는 표제어만 추가하면 되게 하고 있음
# - StopWordsRemover는 nlp 함수가 아니라서, annotation이 아니라서, finalizer후에 사용해줘야 함.
# - nlp에서는 순수하게 자연어를 처리하는 것에만 집중하고, ml로 넘어와서, 사용하고자 하는 목적에 맞춰서 불필요한 단어를 제거해서, nlp에 없는 건가?
from pyspark.ml.feature import StopWordsRemover

# is, from, of, i, me, my등의 삭제하고자 하는 단어 리스트
stopwords = StopWordsRemover.loadDefaultStopWords('english')

stopwords_remover = StopWordsRemover(
    inputCol='normalized',
    outputCol='terms',
    stopWords=stopwords)


#%% larger_pipeline
#pipeline은 다른 pipeline을 가질 수 있음
larger_pipeline = Pipeline(stages=[
    custom_pipeline,
    stopwords_remover
]).fit(texts)

#%% LightPipeline
# DataFrame을 transform하는 것이 아닌 텍스트를 annotate 할 수 있음.
# 그런데, stopwords_remover의 output이 안나오는 걸 보면, nlp annotator들만 되는듯.
from sparknlp.base import LightPipeline
light = LightPipeline(larger_pipeline)
light_result = light.annotate("We are very happy about Spark NLP")