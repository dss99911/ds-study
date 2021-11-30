
# 검색
# - Introduction to Information Retrieval
#   - https://nlp.stanford.edu/IR-book/
# - Apache Lucene : 오픈소스 검색엔진
#   - Apache Solr : 검색 플랫폼
#   - Elasticsearch : 검색 플랫폼
# - Learning to Rank for Information Retrieval, by Tie-Yan Liu (Springer)
#   - https://link.springer.com/book/10.1007/978-3-642-14267-3


# inversed-index
# 단어별로 문서의 index를 가지는 것
# spark를 검색으로 크게 활용되지는 않으므로, 간단하게, 빅데이터 내의 특정 단어를 rank가 높은 순으로 검색 할 수 있게만 하기
# 1. inversed index 만들기
# 2. query를 받으면, inversed index를 통해, 문서를 찾고, 문서들을 rank 높은 순으로 정렬

from spark.nlp.annotator import *
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.sql.types import *

#%%
from pyspark.sql.types import Row
search_model = Pipeline(stages=[
    larger_pipeline,
    CountVectorizer(inputCol='terms', outputCol='tf'),
    IDF(inputCol='tf', outputCol='tfidf'),
]).fit(texts)

def indexed(df: DataFrame) -> DataFrame:
    """add index column"""
    return df.rdd.zipWithIndex().map(
        lambda row_index: Row(
            index=row_index[1],
            **row_index[0].asDict())
    ).toDF()


def inversed_index(df: DataFrame) -> DataFrame:
    """
    df contains 'index', 'text' column
    return DataFrame "term", "documents"

    """

    df_w_terms = larger_pipeline.transform(df)
    return df_w_terms \
        .selectExpr('index', 'explode(terms) AS term') \
        .groupBy('term').agg(collect_set('index').alias('documents'))
#%%
from spark.ml.util import *

def find_docs(spark: SparkSession, query: str, inversed_index: DataFrame, indexed_document: DataFrame, size=10):
    query = spark.createDataFrame([
        (query,)
    ], ["text"])

    # query terms
    terms = larger_pipeline.transform(query).select(explode("terms").alias("term")).distinct()

    filtered_indexes = terms.join(inversed_index, "term")
    # documents containing any query terms
    filtered_indexes = filtered_indexes.select(explode("documents").alias("index"))
    filtered_indexes = filtered_indexes.distinct()

    filtered_document = filtered_indexes.join(indexed_document, "index")

    vocabulary = search_model.stages[-2].vocabulary

    to_vocabulary = udf(lambda i: vocabulary[i])
    # find tfidf for each document ->
    result = search_model.transform(filtered_document) \
        .withColumn("tfidf_index", sparse_vector_indices("tfidf")) \
        .withColumn("tfidf_value", sparse_vector_values("tfidf")) \
        .withColumn("tfidf", explode(arrays_zip(col("tfidf_index"), col("tfidf_value")))) \
        .selectExpr('text', 'index', "tfidf.tfidf_index", "tfidf.tfidf_value") \
        .withColumn("term", to_vocabulary("tfidf_index")) \
        .join(terms, "term") \
        .sort(desc("tfidf_value")) \
        .limit(size) \
        .select("index", "text")

    _print_search_result(result, terms.collect())
#%%

def _print_search_result(df: DataFrame, terms):
    # todo terms와 query 중 어떻게 사용하지?
    import builtins
    for index, text in df.toLocalIterator():
        lines = text.split('\n')
        print("index:", index, 'length:', len(text))
        for line_number, line in enumerate(lines):
            if any(builtins.filter(lambda t: t in line, terms)):
                print(line_number, line)

#%%

# indexed_sample = indexed(example_alt_atheism)
# inversed_index_sample = inversed_index(indexed_sample).cache()
find_docs(spark, "people", inversed_index_sample, indexed_sample, 1)
#%%
from spark.util.util import *
from pyspark.sql import Row
from pyspark.ml import Pipeline
from spark.nlp.example import *
import sparknlp
# from sparknlp import DocumentAssembler, Finisher
# from sparknlp.annotator import *

# spark = sparknlp.start()

# texts = spark.sparkContext.wholeTextFiles("data/mini_newsgroups/*")
#
# schema = StructType([
#     StructField('path', StringType()),
#     StructField('text', StringType()),
# ])
#
# texts = spark.createDataFrame(texts, schema=schema).cache()

# texts.filter(col("path").like("%/alt.atheism/%"))
#%%

def indexed(df: DataFrame) -> DataFrame:
    """add index column"""
    return df.rdd.zipWithIndex().map(
        lambda row_index: Row(
            index=row_index[1],
            **row_index[0].asDict())
    ).toDF()
re = indexed(example_alt_atheism)
# dfs= example_alt_atheism.rdd.zipWithIndex().map(
#     lambda row_index: Row(
#         index=row_index[1],
#         **row_index[0].asDict())
# ).toDF()