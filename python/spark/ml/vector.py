from pyspark.ml.linalg import Vectors
from spark.ml.util import *
from spark.read import *


dense = Vectors.dense([0, 1, 0, 5.5])

sparse = Vectors.sparse(4, {1: 1.0, 3: 5.5})

vectors = spark.createDataFrame([
    (dense, sparse),
], ['d', "s"])


def add_vector_vocab(df, vector_column, vocab_column_prefix: str, vocab_list: list):
    return df.withColumn("vector_temp_column", vector_to_array(col(vector_column))) \
        .select(df.columns + [col("vector_temp_column")[i].alias(f"{vocab_column_prefix}_{v}") for i, v in enumerate(vocab_list)]) \
        .drop("vector_temp_column")

vocab = ['a', 'b', 'c', 'd']
add_vector_vocab(vectors, "s", "vocab", vocab).show()

