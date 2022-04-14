# ML Model (Supervised Learning)

## Linear Model
피쳐가 독립적이라는 가정
피쳐 수를 줄일 수 있는 만큼 줄여서 독립적으로 의미있는 피쳐만 활용하는게 좋다 

### Naive Bayes
![img.png](img.png)
- 모든 피쳐가 독립적이라는 순수한(naive) 가정하에 쓰는 모델
- 여러 단어가 조합하여 feature importance가 높아지지 않는 경우에 사용
- 실제 자연어는 단어와 단어가 독립적일 수 없지만, TF.IDF와 비슷하여, 인기가 있다고 함.
- 스팸 메일 필터, 텍스트 분류, 감정 분석, 추천 시스템 등에 광범위하게 활용되는 분류 기법
- k : 클래스 수
- N : 피쳐 수
- P(term|class)는 term이 있을 때, class일 확률
- P(class) 전체 중 class의 비율
- P(class|term1,term2,termN) : term1~N이 있을 때, class의 확률
- 특정 클래스의 값 = (클래스 비율) * (각 term이 있을 때 class의 확률)
- 특정 클래스의 값 / 전체 클래스의 값의 합 = 특정 클래스의 확률
- Product Notation
  - Sigma는 덧셈을 하는 반면 이건 곱셈

## Decision, regression tree
피쳐 독립성을 가정하지 않음
회소한 경우에 가중치가 높게 측정되야 하는 경우도 있는데(IDF), 이 모델들은 회소한 것보다, 자주 발생하는 피쳐에 의해 영향을 받을 가능성이 높다고 함.
이러한 단점을 극복하기 위해서 stop-word removing을 적극적으로 해야 한다고 함.
random forest나 gradient boosted tree를 쓰면 이러한 어려움을 완화 할 수 있다고 함

### Random Forest
- 비선형적
- 여러 피쳐를 조합하여 feature importance가 높아 지는 경우도 찾을 수 있음

## XGBoost
label이 특정 범위인 경우
- https://xgboost.readthedocs.io/en/stable/tutorials/aft_survival_analysis.html

과적합시
- learning_rate을 낮추고 n_estimators를 높여줍니다. (이 둘은 같이 움직입니다)
- max_depth 값을 낮춥니다.
- min_child_weight 값을 높입니다.
- gamma 값을 높입니다.
- subsample, colsample_bytree 값을 조정합니다.

파라미터
- https://hwi-doc.tistory.com/entry/%EC%9D%B4%ED%95%B4%ED%95%98%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EC%9E%90-XGBoost
- num_boost_round (10): 해당 횟수만큼 반복
- early_stopping_rounds: 이 횟수 만큼 반복을 해도 성능향상이 없으면 중단. 
  - 사용하려면 eval 데이터 셋을 입력해야함.
  - 과적합을 방지할 수 있음, n_estimators 가 높을때 주로 사용.
  - https://machinelearningmastery.com/avoid-overfitting-by-early-stopping-with-xgboost-in-python/
- n_estimators (100): 트리 갯수
- learning_rate (0.1)

## Light GBM
https://assaeunji.github.io/machine%20learning/2021-01-07-xgboost/
- 학습시간이 짧음
- 비대칭 트리 : 트리의 균형을 유지하지 않고, 최대 손실값을 갖는 리프 노드를 지속적 분할
- 과적합 : 손길 값이 큰데에는 이유가 있을 텐데, 지속적으로 리프 노드를 지속 분할하여, 과적합이 쉽게 발생할 수 있음. max_depth를 설정하여, 과적합 방지 가능

# 사용 케이스
## 분류 회귀 문제
로지스틱 회귀, 나이브 베이즈, 의사결정 트리가 인기 있다고 함.
의사결정 트리는 단어와 단어가 연관성이 클 때 쓰면 좋을듯.


