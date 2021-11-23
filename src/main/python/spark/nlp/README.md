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

## Performance
- emr spark-RAPIDS 텐서플로우 딥러닝의 경우 GPU를 사용하면 성능이 10배 빨라진다고.
- docs: https://nvidia.github.io/spark-rapids/
- EMR guide: https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-rapids.html


## Issue
- supported spark version
  - https://github.com/JohnSnowLabs/spark-nlp#apache-spark-support
  - 버전이 안 맞으면(3.2.0 최신) 
  - `java.lang.NoClassDefFoundError: org/json4s/package$MappingException` 에러 남

## Study
- Demo : https://nlp.johnsnowlabs.com/demos
- learn : https://nlp.johnsnowlabs.com/learn


## Alternative
- [spaCy](https://spacy.io/)도 있지만, 분산처리를 지원하는 sparkNLP가 요즘 대세라고 함.
