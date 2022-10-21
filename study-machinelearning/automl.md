# Auto ML


## PyCaret
https://pycaret.gitbook.io/docs/get-started/tutorials
https://towardsdatascience.com/5-things-you-are-doing-wrong-in-pycaret-e01981575d2a

장점
- 심플함
- 여러 모델들의 성능 비교
- spark에서 병렬 처리
- databricks에서 autoML로 채택

단점
- 전처리 및 피쳐 분석하는 setup이 시간이 너무 오래 걸림
  - 모델 비교는 다중 core에서 돌아가는 반면,
  - setup은 단일 core에서 돌아감
  - Mac M1에서 안돌아감
    - Library not loaded: '/usr/local/opt/libomp/lib/libomp.dylib'
    - libomp doesn't support arm64.

## AutoGluon

장점
- AWS에서 지원.