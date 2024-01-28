# Auto ML


## PyCaret
https://pycaret.gitbook.io/docs/get-started/tutorials
https://towardsdatascience.com/5-things-you-are-doing-wrong-in-pycaret-e01981575d2a

장점
- 심플함
- 여러 모델들의 성능 비교
- spark에서 병렬 처리
  - https://towardsdatascience.com/scaling-pycaret-with-spark-or-dask-through-fugue-60bdc3ce133f
    - 데이터가 큰 경우, 특정 컬럼을 파티션으로 분할에서 파티션별로 하위 모델을 만들도록 하는 예제(성별, 나이대 별로 모델을 만들어서, 서빙시 요청에 맞는 모델을 사용)
    - 모델 학습시 병렬 학습을 하는 건 아니고, 각 알고리즘별로 병렬 처리하는 것도 아니고, 데이터를 특정 파티션 컬럼으로 분할해서, 파티션별로 모델을 만들어서 학습하는 것.
    - 파티션별로 모델을 분할해서 학습하는게 적절하다면, 이걸 쓰기.
    - 좀 수정하면, 각 알고리즘별로 분산 처리도 가능할 수도 있겠지만, 각 모델별 알고리즘 별 소요시간도 다를 거라서, sagemaker 스텝으로 분할하는게 좋을듯..?
- databricks에서 autoML로 채택

단점
- 전처리 및 피쳐 분석하는 setup이 시간이 너무 오래 걸림
  - 모델 비교는 다중 core에서 돌아가는 반면,
  - setup은 단일 core에서 돌아감
  - 피쳐가 좀만 많아져도, 테스트 불가
  - Mac M1에서 안돌아감
    - Library not loaded: '/usr/local/opt/libomp/lib/libomp.dylib'
    - libomp doesn't support arm64.

## AutoGluon

장점
- AWS에서 지원.
- model quality 설정 가능(빠르게 테스트 가능)
- 학습 시간 limit설정 가능(하지만, limit이 작으면, 여러 알고리즘을 사용하지않음)
- ensemble 모델도 사용 
- 메모리 부족시, 커널이 안 죽음

단점
- 에러가 나면, CPU를 계속 사용하고, 종료를 안함
- RandomForestMSE에서 오래걸림
- feature importance 오래 걸림



## Autopilot Ensemble
장점
- UI, 사용성이 좋음
- Autogluon과 동일한 장점
- 학습 시간 limit설정 가능
- test data 자동 분리
단점
- model quality 설정 불가 등 커스터마이징 어려움
- 도중에 작동 안될 때 있음


## Sagemaker에 적용
Emr에서 pycaret으로 분산처리하려면
데이터 파티셔닝으로 작은 모델을 여러개 만들거나 알고리즘별로 분산해서 처리해야되는데,

큰모델이 필요한 경우 해결이 어렵고,
알고리즘별로 분산처리를 한다면, 소요시간이 재각각일 거라, spark분산 처리를 제대로 활용하기 어렵다

사용한다면, sagemaker pipeline에서, 모델별, 알고리즘별로 스텝을 나눠서 파이프라인을 구성해서 하는게 좋을듯. 이렇게 할 경우 성능이 안나오는 모델이나 알고리즘의경우 인스턴스 업그레이드 가능.
하지만 하나의 모델을 분산 학습은 어렵지만, 이 경우, 별도로 분산이 지원되는 training step을 추가해서 가능할 듯.


사용 목적
- 신규모델 poc. 작은데이터로 할테니. 이 용도가 적절.

피쳐 중요도 파악. 기존 중요피쳐 데이터로 학습 후, 신규 피쳐와 조인해서 학습 성능비교. xgboost lightgbm을 pyspark에서 수월하게 사용할 수 있게 하기

기존 모델의 알고리즘이 적절한지 확인하기. 다른 알고리즘과 비교해 어느정도 효과가 있는지 파악

모델 성능의 지속적 파악(월별 동일 모델의 성능, 월별 신규 학습 모델과 기존 모델의 성능차이. Develop브랜치의 모델과 master 브랜치의 성능차이로 신규모델 배포 필요성 파악)

피처그룹별 모델. 유저 특성별 모델 등으로 모델 학습에 필요한 데이터 수를 줄이고 많은 모델을 만들기. 이건 좋은 방법론인지 공부가 필요할 듯