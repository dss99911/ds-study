# https://nlp.johnsnowlabs.com/docs/en/pipelines
# https://nlp.johnsnowlabs.com/models

import sparknlp
from sparknlp.pretrained import PretrainedPipeline
from pyspark.sql.types import *

#%%
spark = sparknlp.start()

texts = spark.sparkContext.wholeTextFiles("data/mini_newsgroups/*")
schema = StructType([
    StructField('filename', StringType()),
    StructField('text', StringType()),
])
texts_df = spark.createDataFrame(texts, schema)

#%% explain_document_ml

explain_document_pipeline = PretrainedPipeline("explain_document_ml")
annotations = explain_document_pipeline.annotate("We are very happy about SparkNLP")
print(annotations)

#%% explain_document_ml w/ DataFrame.
# 단순 text annotate보다 annotation데이터가 보다 자세하다.

explained_texts_df = explain_document_pipeline.annotate(texts_df, "text")
explained_texts_df.show(n=2, truncate=100, vertical=True)

#%% recognize_entities_dl

from sparknlp.pretrained import PretrainedPipeline

pipeline = PretrainedPipeline('recognize_entities_dl', 'en')
result = pipeline.annotate('President Biden represented Delaware for 36 years in the U.S. Senate before becoming the 47th Vice President of the United States.')
print(result['ner'])
print(result['entities'])

#%% analyze sentiment

pipeline = PretrainedPipeline('analyze_sentimentdl_glove_imdb', 'en')
result = pipeline.annotate("Harry Potter is a great movie.")
print(result['sentiment'])