## 튜닝 방법
1. 데이터 분석 및 전처리
   1. preprocessing
   2. missing value imputation
   3. autocorrelation
2. train, eval, test set 분리
   1. cross validation으로 학습 평가
   2. random split시 데이터가 과적합하게 된다면, 직접 분할하여 평가하기
   3. test set: 학습데이터와 비슷하지 않은 데이터(최근 데이터나, 별도 카테고리 데이터)로 검증
3. parameter 선정
   1. 풀고자 하는 문제에 적합한 파리미터를 선정한다.
   2. 예측하려는 데이터가 학습한 데이터와 전혀 다를 수 있는 경우, 보수적으로 과적합을 줄이는게 좋다.
   3. grid search로 큰 범주의 parameter 찾기.
   4. 각각의 parameter들을 하강 경사법과 비슷한 방식으로 미세 조정
4. 검증
   1. 과적합 체크
      1. train, eval metric의 round별 분포를 보고, train 점수는 올라가는데, eval점수는 안 올라간다면, 과적합 의심.
   2. feature importance확인, 
      1. importance가 거의 없는 피쳐들을 제거한다(학습에 오히려 방해됨)
      2. 중요 피쳐들이 레이블과 상관관계가 있는지 이해해보기
         1. 의미 없어 보이는 게 높은 importance를 가진다면, 과적합된건 아닌지 의심하고, 의미없는 피쳐를 전처리로 제거
   3. probability의 분포를 확인한다.(이진 분류 문제인데, 0.5근처에 모여있으면, 분류를 제대로 수행 못하고, 0, 1 쪽으로 몰릴 수록 좋은 분포임)
   4. test set 체크
      1. confusion metrix로 어떤 케이스에 많이 틀리는지 확인
      2. 잘못 예측한 케이스들 하나 하나 원인 분석 후 전처리 개선
         1. 도움이 될만한 피쳐를 추가 개발도 고려
   5. probability threshold 정하기. 어떤 메트릭이 중요하냐에 따라, 정한다.
      1. 트랜젝션 여부는 리콜이 중요함


## Parameter Tuning

### Grid Search
- 수동으로 설정한 파라미터드들을, 각 가능한 모든 조합으로 학습시키는 방법
- cross validation과 보통 같이 사용하여, 더 좋은 성능의 파라미터를 찾는 방법
- 데이터 자체가 과적합이 의심될 경우, 데이터를 과적합을 피할 수 있게 분리가 가능하다면, 수동분리하여, 파라미터를 찾는게 더 좋을듯..

### Randomized search
확률 분포에 따라, 각 파라미터들을 임의로 설정하여 학습시키는 방법

### Bayesian search
build a probability model of the objective function and use it to select the most promising hyperparameters to evaluate in the true objective function
https://data-scientist-brian-kim.tistory.com/m/88

