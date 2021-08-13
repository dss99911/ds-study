# Missing Value(결측치) Imputation
- [wiki](https://en.wikipedia.org/wiki/Imputation_(statistics))
- Impute : 죄 오명 등을 전가시키다. 값이 없는건 좋지 않은 것을 다른 값으로 치환 시키는 것. im: in, pute: cut, prone
- 없는 값을 어떻게 대체할 지에 대한 방법론으로 여러가지 방식이 많고, 해당 피쳐에 적절한 imputation을 결정해야 한다.
- 여러 방법론이 있는데, 여러 방법론 중 상관 계수가 높은 방식을 택한다.
- missing value 빈도수도 파악하기

## listwise and pairwise deletion
- [wiki](https://account.jetbrains.com/oauth2/signin?login_challenge=e28f2434a6b24ac5a561ee517436821b)
- 없는 값을 단순 제거 하는 방법
- 값이 없는 경우가 순전히 랜덤인 경우, 이 방식으로 했을 때, bias 가 없기 때문에, 괜찮음.
- 하지만, 샘플 갯수가 줄어듬
- 값이 없는 경우가 랜덤이 아닌 경우, bias 및 잘못된 결과가 나올 수도 있음
- 값이 없는 경우에 bias가 있는지 없는지 판단해 볼 수 있지 않을까? 값이 없는 경우와 label과의 상관 계수를 구하기.
- missing value만 했을 때, 상관 계수가 낮으면, missing value를 제외해서 처리하고, 상관 계수가 높으면, missing value를 포함/제외 해서 상관계수가 높은 것으로 한다.
- 만약 값이 없을 경우에는 알 수 없지만, 값이 있을 경우에는 높은 상관계수를 나타낸다고 하면, 머신러닝 학습할 때, 어떻게 피쳐 값을 넣어줘야 하지? null로 넣으면, null일 땐 결과값이 들쭉날쭉이라, 해당 피쳐의 중요도가 낮다고 인식하는건 아닐까? 하지만 널이 아닌 경우엔 일관성이 있어서,단순 leaner regression만 아니면, 일관된 분포 그룹을 인지할 듯.

## Single imputation
### Mean substitution
- 평균값으로 전가시킴.
- 값이 있을 때, 강한 상관이 있다고 하더라도, 상관계수값을 약화시킴.
- imputation has some attractive properties for univariate analysis but becomes problematic for multivariate analysis.

### Non-negative matrix factorization
- [ ] [wiki](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization)

### Regression
- 다른 variables을 토대로, 예측함.
- 다른 variables들이 예측에 도움이 되는 데이터 이면 쓸만 할 듯.
- 해당 variable과 missing value의 상관계수를 토대로 variable을 선정하면 좋을듯.
- 그런데, 두 피쳐를 학습용으로 둘다 쓴다고 하면, 둘다 label과의 상관계수를 구하게 되므로, 굳이 regression을 쓸 필요가 있나 싶음.
- 더큰 noise가 낄 수 있고, residual variance없이 과 정밀한 값이 impute된다.
- Stochastic regression 가 어느정도 성공적이라고 함.

## Multiple imputation
- Single imputation과 달리, 여러개의 imputated value를 통해, 여러개의 결과를 만들어내고,
- 결과들의 평균, 분산, 신뢰구간 등을 고려하여, 결과를 하나로 통합한다.
- Single imputation과 달리 불확실성도 고려함
- flexible하여, randomly missing과 아닌 경우 모두에 사용 가능
- 여러가지 방식이 있음
    - MICE : missing at randome data를 위해 디자인됨.
    - MIDAS : 머신러닝을 사용하는 최근 접근방법. MIDASpy 사용 가능

# Handle Missing Values in Machine Learning
- [reference](https://towardsdatascience.com/7-ways-to-handle-missing-values-in-machine-learning-1a6326adf79e)

- 머신러닝 알고리즘 중 missing value를 지원하는게 있고,안하는게 있음. missing value를 어떤식으로 지원하는지도 확인 필요
    - k-NN
    - Naive Bayes
    - RandomForest : work fine for not learnear and categorical
- deep learning : datawig
    - missing value가 있는 컬럼과 그외 컬럼들을 input으로 넣어서, missing value를 impute함.
    

# handle Missing Value by Value type
## categorical
- 단순히 NA를 넣고, randomForest만 돌려도 잘 동작함.
## numeric
- mean값을 넣으면, 상관계수가 약해짐
- categorical처럼 numeric도 모델이 그룹화 하여 인식하는지 확인필요
- 그룹화가 안되면, 값을 cateogorical하게 값을 치환해야 할듯.

## ordinal