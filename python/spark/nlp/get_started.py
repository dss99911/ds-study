#%%
import sparknlp
from sparknlp.pretrained import PretrainedPipeline

spark = sparknlp.start()

print("Spark NLP version: {}".format(sparknlp.version()))
print("Apache Spark version: {}".format(spark.version))

#%%
sentences = [
    ['Hello, this is an example sentence'],
    ['And this is a second sentence.']
]

# spark is the Spark Session automatically started by pyspark.
data = spark.createDataFrame(sentences).toDF("text")


#%% PretrainedPipleline

# Download the pretrained pipeline from Johnsnowlab's servers
explain_document_pipeline = PretrainedPipeline("explain_document_ml")

# Transform 'data' and store output in a new 'annotations_df' dataframe
explained_texts_df = explain_document_pipeline.transform(data)
# explained_texts_df = explain_document_pipeline.annotate(data, "text") # column이 text가 아닌 경우.

# Show the results
explained_texts_df.show()

#%% Finisher
# annotate 결과 값은 annotatorType, begin, end, result, metadata 등 다양한 값을 제공 해준다.
# 이걸 정리해서 활용하기는 쉽지 않아서, Finisher라는 것을 통해 정리된 결과 값을 만들어 내는 것 같음

from sparknlp import Finisher

finisher: Finisher = Finisher()
finisher = finisher.setInputCols("lemmas")
finisher = finisher.setOutputCols("lemmata")
finisher = finisher.setCleanAnnotations(True)  # input cols를 지우는 것인듯..?
finisher = finisher.setAnnotationSplitSymbol(' ')
finisher = finisher.setOutputAsArray(False)  # 배열 대신 문자열 출력
finished_text_df = finisher.transform(explained_texts_df)
finished_text_df.show(n=1, truncate=100, vertical=True)
result = finished_text_df.take(1)
