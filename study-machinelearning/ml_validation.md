# Model Validation

## Train test set split
학습 결과를 테스트하기 위해서, train데이터과 test 데이터를 분리한다.

## Train, validation, Test set split
파라미터 튜닝시에 사용하는 검증 테스트셋을 validation set이라고 함
파라미터 튜닝시의 데이터 셋이 해당 파라미터에셔 우연히 성능이 좋게 나온 걸 수 있으므로, 파라미터가 결정되고나서, 최종적으로 test 셋으로 성능이 잘 나오는지 확인한다.

이 외에 evaluation set이라는 용어도 사용 되는데,
- 학습 라운드별로, evaluation을 통해, 라운드가 계속 될 수록, 성능향상이 되는지 파악하고, 
- 학습 accuracy는 올라가는데, eval accuracy는 안 올라가면, overfitting이 된 건지 파악할 수 있고, 
- eval성능 향상이 안되는 시점에, 학습을 중단도 가능
- https://xgboost.readthedocs.io/en/stable/jvm/xgboost4j_spark_tutorial.html#early-stopping

## Cross Validation
- (train, test) set을 k fold 만큼 분리하여, 각 fold 모델의 성능 평균을 파라미터별로 구한다
- 많이 분리하여, (train, test) set이 잘못 분리되어, overfitting이 되는 것을 방지함
- 보통 grid search를 통해 각 파라미터별 성능을 구할 때 같이 사용함
- 보통 k=3, 10 을 사용한다고 함
