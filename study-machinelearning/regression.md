# Regression

## 평가

https://velog.io/@dlskawns/Linear-Regression-%EC%84%A0%ED%98%95%ED%9A%8C%EA%B7%80%EC%9D%98-%ED%8F%89%EA%B0%80-%EC%A7%80%ED%91%9C-MAE-MSE-RMSE-R-Squared-%EC%A0%95%EB%A6%AC

- MAE(Mean Absolute of Errors) 평균절대오차
  - 예측값 - 실제값의 절대값의 평균
- MSE(Mean Square of Errors) 평균제곱오차
  - 분산과 비슷. (예측값 - 실제값)의 제곱의 평균
  - 오차가 심할 수록, 더 오차가 커져서, 오차가 크면 더 안 좋은 케이스에 적용하면 좋을 듯.
- RMSE(Root Mean Square of Errors) 평균제곱오차제곱근
  - 표준편차와 비슷. (예측값 - 실제값)의 제곱의 루프의 평균
- MSLE: Mean squared logarithmic error
  - 0일 수록 좋음.
  - 오차와 실제 값의 비율이 같으면, MSLE값도 비슷.
  - 위의 방식들은, 실제 값과 오차의 비율은 고려하지 않음.(집 값등은 값이 클 수록, 오차도 클 수 있음)
  - https://peltarion.com/knowledge-center/modeling-view/build-an-ai-model/loss-functions/mean-squared-logarithmic-error-(msle)
- R2(R Squared Score) 결정계수
  - 결정계수는 실제 관측값의 분산대비 예측값의 분산을 계산하여 데이터 예측의 정확도 성능을 측정하는 지표
  - 실제 값과 오차의 비율이 같으면, r2 값도 같음

어떤 지표를 쓰든, y평균값으로 구한 지표를 기준으로 얼마나 좋은지 비교.