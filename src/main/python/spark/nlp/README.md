# Spark NLP

## install : 
- https://nlp.johnsnowlabs.com/docs/en/install
  - colab : https://colab.research.google.com/github/JohnSnowLabs/spark-nlp-workshop/blob/master/jupyter/quick_start_google_colab.ipynb#scrollTo=YkbpOBs6DasA
  - python : https://nlp.johnsnowlabs.com/docs/en/install#quick-install

## model hub 
- https://nlp.johnsnowlabs.com/models

### Explain Document ML : 
- https://demo.johnsnowlabs.com/public/GRAMMAR_EN/
- 문법 등을 체크하고, 각 단어가 문법의 어떤 요소이고 어떤 단어와 연관이 있는지 확인가능

## Annotator
- DocumentAssembler :
- Sentense Segmenter :
- Tokenizer
- SpellChecker
- Stemmer : 어간 생성
- Lemmatizer : 표제어 (are의 경우 be) 생성
- POS TAGGER : 품사 생성

## Issue
- supported spark version
  - https://github.com/JohnSnowLabs/spark-nlp#apache-spark-support
  - 버전이 안 맞으면(3.2.0 최신) 
  - `java.lang.NoClassDefFoundError: org/json4s/package$MappingException` 에러 남

## Study
- Demo : https://nlp.johnsnowlabs.com/demos
- learn : https://nlp.johnsnowlabs.com/learn