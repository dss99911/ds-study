## Term Frequency

### CountVectorizer
- bag-of-words 단어가방. 단어별로 가방이 있고, 가방은 단어의 수를 의미
- 단어를 숫자로 변환. 총 단어 수 및, 각 단어 별, 갯수 리턴
- 전처리를 안했을 경우, HashingTF가 CounterVectorizer보다 더 좋다고 함

### HashingTF
- hash로 단어를 만들어서, vocab 목록을 볼 수 없음.
- 고정 사이즈
- hash로 만들기 때문에 처리 속도가 빠름.

#### 특정 분야의 용어로 어휘를 제한하기
- (의학용어의 경우 UMLS라는 오픈 리소스 사용 가능)
- 장 : 과적합을 피함(의미 있는 단어들로만 학습하기 때문에, 비슷한 문서로만 학습해도, 어느정도 효과가 있다는 의미 인듯)
- 단 : 일반화 되지 않는 특성이 있는 경우, 반영하지 못함 (용어에 없는 단어가 의미를 지닐 때, 이걸 반영하지 못함)
- CounterVectorizer fit할 때, 해당 용어로 fit하면 어휘 제한 가능

#### minDF : minimum document frequency.
- vocabulary에 등록이 되려면, 최소한 minDF 갯수 이상의 문서가 있어야 한다는 의미.
- 보통 가중치는 어휘가 적은 문서에서 발생할 때, 높게 주는데(IDF), 이 설정은 어찌 보면 그와 반대로 보일 수도 있지만,
- classification을 하려고 하고 있고, 한 레이블당 100개의 문서가 있으므로,
- 너무 적은 문서에서 나오는 용어는 레이블과 관련없는 오히려 의미 없는 용어로 해석할 수도 있으므로,
- classification을 할 때, 각 레이블 당 문서의 수에 맞춰서 적절히 설정해주면 될듯.? default 1

- fit이후, tf_model.vocabulary[ix] 로 vector와 word맵핑 확인 가능
- vocabulary는 Document frequency가 높은 순으로 정렬되어 있음

## IDF(Inverse Document Frequency)
- DF : 문서의 빈도(단어가 얼마나 많은 문서에 나오는가)에 따라 단어의 가중치를 줌
- IDF : 문서의 빈도가 낮은 경우에 가중치가 높음
- tf에서의 갯수 값을 가중치 값으로 변경(fit할때, 각 단어별 IDF값이 정해지고, transfer로 특정 문서의 tfidf를 구할 때, tf * idf를 함)
- IDF사용 이유 : topic을 찾을 때, 문서 빈도가 낮은 단어가 해당 문서의 topic과 관련있을 가능성이 높으므로 idf를 사용.


### minDocFreq : minimum number of documents. default 0.
- minDF와 같이 설정해줌. 비슷한 의미 같은데, 왜 하는 건진 잘 모르겠음
