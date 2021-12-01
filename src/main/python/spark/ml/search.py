
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

#%% write model

from spark.ml.util import *
from spark.nlp.example import *
from pyspark.ml.feature import CountVectorizer, IDF

larger_pipeline = PipelineModel.load("pipeline/nlp")

search_model: PipelineModel = Pipeline(stages=[
    larger_pipeline,
    CountVectorizer(inputCol='terms', outputCol='tf'),
    IDF(inputCol='tf', outputCol='tfidf'),
]).fit(texts)

search_model.write().overwrite().save("pipeline/nlp-query")
#%% load model
from spark.nlp.example import *
from spark.ml.util import *
from pyspark.sql.types import Row

search_model = PipelineModel.load("pipeline/nlp-query")
larger_pipeline = PipelineModel.load("pipeline/nlp")

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


def tfidf_docs(document: DataFrame):
    """return Datafrom contains 'tfidf_index', 'tfidf_value'"""
    return search_model.transform(document).select(document.columns + ["tfidf"]) \
        .withColumn("tfidf_index", sparse_vector_indices("tfidf")) \
        .withColumn("tfidf_value", sparse_vector_values("tfidf")) \
        .drop("tfidf")


def tfidf_index_to_vocabulary(tfidf: DataFrame, col_name: str):
    """return with 'term' column"""
    vocabulary = search_model.stages[-2].vocabulary
    to_vocabulary = udf(lambda i: vocabulary[i])
    return tfidf.withColumn("term", to_vocabulary(col_name))

#%%
def find_docs(spark: SparkSession, query: str, inversed_index: DataFrame, tfidf_document: DataFrame, size=10):
    query = spark.createDataFrame([
        (query,)
    ], ["text"])

    # query terms
    terms = larger_pipeline.transform(query).select(explode("terms").alias("term")).distinct().cache()
    list_terms = terms.rdd.flatMap(lambda r: r).collect()
    print(f"query term : {list_terms}")

    filtered_indexes = terms.join(inversed_index, "term")
    # documents containing any query terms
    filtered_indexes = filtered_indexes.select(explode("documents").alias("index"))
    filtered_indexes = filtered_indexes.distinct()

    filtered_document = filtered_indexes.join(tfidf_document, "index")

    # find tfidf for each document ->
    result = filtered_document \
        .withColumn("tfidf", explode(arrays_zip(col("tfidf_index"), col("tfidf_value")))) \
        .selectExpr('text', 'index', "tfidf.tfidf_index", "tfidf.tfidf_value")

    result = tfidf_index_to_vocabulary(result, "tfidf_index") \
        .join(terms, "term") \
        .sort(desc("tfidf_value")) \
        .limit(size) \
        .select("index", "text")

    # find query and term both
    search_term = set(query.rdd.flatMap(lambda r: r).collect() + list_terms)
    _print_search_result(result, search_term)


def _print_search_result(df: DataFrame, terms):
    # todo terms와 query 중 어떻게 사용하지?
    import builtins
    for index, text in df.toLocalIterator():
        print("index:", index, 'length:', len(text))
        lines = text.split('\n')
        for line_number, line in enumerate(lines):
            if any(builtins.filter(lambda t: t in line, terms)):
                print(line_number, line)

#%% search query

tfidf_sample = tfidf_docs(indexed(example_alt_atheism)).cache()
inversed_index_sample = inversed_index(tfidf_sample).cache()

find_docs(spark, "addresses", inversed_index_sample, tfidf_sample, 10)

#%% analyze result
tfidf_sample.filter("index = 8").show(100, False)
# inversed_index_sample.filter("term = 'address'").show(100, False)

# test_voca = tfidf_sample.filter("path like '%53538%'")\
#     .select(explode("tfidf_index").alias("tfidf_index"))
# tfidf_index_to_vocabulary(test_voca, "tfidf_index").show(100, False)
