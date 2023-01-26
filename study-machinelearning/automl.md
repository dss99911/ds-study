# Auto ML


## PyCaret
https://pycaret.gitbook.io/docs/get-started/tutorials
https://towardsdatascience.com/5-things-you-are-doing-wrong-in-pycaret-e01981575d2a

장점
- 심플함
- 여러 모델들의 성능 비교
- spark에서 병렬 처리
  - https://towardsdatascience.com/scaling-pycaret-with-spark-or-dask-through-fugue-60bdc3ce133f
    - 특정 파티션별로 분할에서 파티션별로 모델을 만들도록 하는 예제
    - 모델 학습시 병렬 학습을 하는 건 아니고, 각 알고리즘별로 병렬 처리하는 것도 아니고, 데이터를 특정 파티션 컬럼으로 분할해서, 파티션별로 모델을 만들어서 학습하는 것.
    - 파티션별로 모델을 분할해서 학습하는게 적절하다면, 이걸 쓰기.
    - 좀 수정하면, 각 알고리즘별로 분산 처리도 가능할지..?
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