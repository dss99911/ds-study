from pyspark.ml import Pipeline
from sparknlp.training import POS
import nltk
from spark.nlp.example import *

nltk.download('brown')
from nltk.corpus import brown

#%% save pos
with open('tagged_brown.txt', 'w') as out:
    for fid in brown.fileids():
        for sent in brown.tagged_sents(fid):
            for token, tag in sent:
                out.write('{}_{} '.format(token, tag))
            out.write('\n')

#%% load pos
tag_data = POS().readDataset(spark, 'tagged_brown.txt', '_', 'tags')
td = tag_data.limit(10).toPandas().to_dict()

#%% learning


from sparknlp.annotator import Tokenizer, PerceptronApproach, SentenceDetector
from sparknlp import DocumentAssembler, Finisher

assembler = DocumentAssembler() \
    .setInputCol('text') \
    .setOutputCol('document')
sent_detector = SentenceDetector() \
    .setInputCols(['document']) \
    .setOutputCol('sentences')
tokenizer = Tokenizer() \
    .setInputCols(['sentences']) \
    .setOutputCol('tokens')

pos_tagger = PerceptronApproach() \
    .setNIterations(1) \
    .setInputCols(["sentences", "tokens"]) \
    .setOutputCol("pos") \
    .setPosCol("tags")

finisher = Finisher() \
    .setInputCols(['tokens', 'pos']) \
    .setOutputCols(['tokens', 'pos']) \
    .setOutputAsArray(True)

pipeline = Pipeline().setStages([
    assembler, sent_detector, tokenizer, pos_tagger, finisher
])

pipeline = pipeline.fit(tag_data)

