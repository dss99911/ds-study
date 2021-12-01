from collections import Counter
from spark.util.util import *
from pyspark.ml import PipelineModel, Pipeline

def collect_counter(df: DataFrame, col_name: str, get_label=lambda i: i) -> Counter:
    counts = Counter()

    for row in df.toLocalIterator():
        for ix, count in zip(row[col_name].indices, row[col_name].values):
            counts[get_label(ix)] += count
    return counts


def sparse_vector_indices(col_name):
    sparse_vector_indices = udf(lambda v: v.indices.tolist(), ArrayType(IntegerType()))
    return sparse_vector_indices(col_name)


def sparse_vector_values(col_name):
    sparse_vector_values = udf(lambda v: v.values.tolist(), ArrayType(DoubleType()))
    return sparse_vector_values(col_name)
#%%