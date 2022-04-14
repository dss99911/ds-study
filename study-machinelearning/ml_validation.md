# Model Validation

## Train test set split
학습 결과를 테스트하기 위해서, train데이터과 test 데이터를 분리한다.

## Train, Evaluation, Test set split
evaluation이 추가되었는데,
- 학습 라운드별로, evaluation을 통해, 라운드가 계속 될 수록, 성능향상이 되는지 파악하고, 
- 학습 accuracy는 올라가는데, eval accuracy는 안 올라가면, overfitting이 된 건지 파악할 수 있고, 
- eval성능 향상이 안되는 시점에, 학습을 중단도 가능

## Cross Validation
- train, test set을 임의로 분리하여, 지정한 횟수만큼 학습을 하고, 그 결과를 보여줌으로 써, 성능의 평균치를 제공.
- 질문 : train, test set이 잘못 분리되어, overfitting이 되거나, 성능 저하가 발생할 수도 있지 않나? 보통 hyper parameter조정과 같이 쓰는 용도로 많이 쓰는듯?