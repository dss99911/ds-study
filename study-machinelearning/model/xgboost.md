# XGBoost
- https://xgboost.readthedocs.io/en/stable/index.html
- spark tutorial: https://xgboost.readthedocs.io/en/stable/jvm/xgboost4j_spark_tutorial.html
- repo : https://mvnrepository.com/artifact/ml.dmlc/xgboost4j-gpu_2.12/1.3.1
- [한국 설명](https://brunch.co.kr/@snobberys/137)

## 모델 이해
tree
- 소규모 분류기.
- 가지마다 피쳐 조건을 설정하여, 데이터들을 분류하는 방법.
- leaf node에 score를 매겨, 특정 피쳐 조건들의 경우, 어떤 점수를 가지는지를 구함

forest
- 여러 tree들을 함께 사용

boosting
- 각 tree들에 가중치를 두어, 각 데이터에 대한 스코어를 산출해내고, 가중치를 조정하는 작업

장점
- 과적합이 잘 일어나지 않음 (greedy algorithm을 이용한 자동 가지치기)

## 기능
### categorical data
- 기존에는 onehot encoding으로 데이터를 변환해줘야 했다면, 지금은 그럴필요 없다고 함
- https://xgboost.readthedocs.io/en/latest/tutorials/categorical.html

### 멀티 레이블
- 비 배타적 레이블이 여러개 같이 존재하는 경우.(예: 영화 장르에는 코미디, 액션 등 중복 가능)
- https://xgboost.readthedocs.io/en/latest/tutorials/multioutput.html

### label이 특정 범위인 경우
- https://xgboost.readthedocs.io/en/stable/tutorials/aft_survival_analysis.html

## 파라미터
- https://xgboost.readthedocs.io/en/latest/parameter.html
- https://hwi-doc.tistory.com/entry/%EC%9D%B4%ED%95%B4%ED%95%98%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EC%9E%90-XGBoost
### 과적합
- 트리의 가지가 많을 수록 과적합하기 쉬움(모든 데이터를 각각 구별하는 조건을 만들었을 때 가장큰 과적합이 되는 걸 생각하면 될듯.)
- eta을 낮추고 n_estimators를 높여줍니다. (이 둘은 같이 움직입니다)
- max_depth 값을 낮춥니다.
- min_child_weight 값을 높입니다.
- gamma 값을 높입니다.
- subsample, colsample_bytree 값을 조정합니다.


### 일반 파라미터
- booster: 부스터 구조. gbtree, gblinear, dart
- num_feature : 피쳐 차원 수를 정할 때. 중요 피쳐 몇개만 선정할 때 쓰는 건가?

### boosting 파라미터
- eta(learning rate [0,1], default 0.3): 매 부스팅시마다, 트리에 가중치 조정 크기
- gamma(default 0): 값이 크면, 트리 깊이가 줄어들어, 보수적(보수적이라는 건, 성능은 낮게 나오지만, 과적합은 줄일 수 있다는 의미)
- max_depth(default 6): 트리의 최대 깊이. 낮을 수록 보수적
- lambda: L2 Regularization Form에 달리는 weights. 클수록 보수적
- alpha: L1 Regularization Form에 달리는 weights. 클수록 보수적

### 학습 과정 파라미터
- objective: 목적함수. reg:linear(회귀), binary:logistic(이진 논리), multi:softprob(다중 클래스)
- eval_metric: 평가 함수. binary -> "auc"
- num_round (default 10): 해당 횟수만큼 boosting 반복. epoch과 동일

### 기타 파라미터
- early_stopping_rounds: 이 횟수 만큼 반복을 해도 성능향상이 없으면 중단.
    - 사용하려면 eval 데이터 셋을 입력해야함.
    - 과적합을 방지할 수 있음, n_estimators 가 높을때 주로 사용.
    - https://machinelearningmastery.com/avoid-overfitting-by-early-stopping-with-xgboost-in-python/
- n_estimators (100): 트리 갯수

