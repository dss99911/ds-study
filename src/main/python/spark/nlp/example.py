import sparknlp
from spark.util.util import *

spark = sparknlp.start()
# RDD containing filepath-text pairs
texts = spark.sparkContext.wholeTextFiles("data/mini_newsgroups/*")

schema = StructType([
    StructField('path', StringType()),
    StructField('text', StringType()),
])

texts = spark.createDataFrame(texts, schema=schema).cache()
example = '''
Nick's right about this.  It's always easier to obtian forgiveness than
permission.  Not many poeple remember that Britan's Kng George III
expressly forbade his american subjects to cross the alleghany/appalachian
mountains.  Said subjects basically said, "Stop us if you can."  He
couldn't.
'''
example = spark.createDataFrame([('.', example)], schema=schema).persist()
#%%

example_alt_atheism = texts.filter(col("path").like("%/alt.atheism/%"))
example_sci_space = texts.filter(col("path").like("%/sci.space/%"))
example_rec_autos = texts.filter(col("path").like("%/rec.autos/%"))
