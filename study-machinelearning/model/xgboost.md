# XGBoost
- https://xgboost.readthedocs.io/en/stable/index.html
- spark tutorial: https://xgboost.readthedocs.io/en/stable/jvm/xgboost4j_spark_tutorial.html

## label이 특정 범위인 경우
- https://xgboost.readthedocs.io/en/stable/tutorials/aft_survival_analysis.html

## 과적합시
- learning_rate을 낮추고 n_estimators를 높여줍니다. (이 둘은 같이 움직입니다)
- max_depth 값을 낮춥니다.
- min_child_weight 값을 높입니다.
- gamma 값을 높입니다.
- subsample, colsample_bytree 값을 조정합니다.

## 파라미터
- https://hwi-doc.tistory.com/entry/%EC%9D%B4%ED%95%B4%ED%95%98%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EC%9E%90-XGBoost
- num_boost_round (10): 해당 횟수만큼 반복
- early_stopping_rounds: 이 횟수 만큼 반복을 해도 성능향상이 없으면 중단.
    - 사용하려면 eval 데이터 셋을 입력해야함.
    - 과적합을 방지할 수 있음, n_estimators 가 높을때 주로 사용.
    - https://machinelearningmastery.com/avoid-overfitting-by-early-stopping-with-xgboost-in-python/
- n_estimators (100): 트리 갯수
- learning_rate (0.1)

