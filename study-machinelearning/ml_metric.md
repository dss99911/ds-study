# Metric

https://towardsdatascience.com/accuracy-precision-recall-or-f1-331fb37c5cb9
https://blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221531940245

일반적으로 문제가 되는 경우를 positive로 설정함
- 연체(positive) 상환(negative)
- 감염(positive) 미감염(negative)

### Accuracy : 정확도.
  - true case / total case
  - positive, negative 무엇이 더 중요하냐와 무관하게, 전체 수 중 맞춘 수를 구하는 것으로 

### Precision : 정밀도. positive예측의 정확도
  - true positive / (true positive + false positive)
  - (양성으로 예측한게) 정확한지. 정확도를 구하는 것.
  - 0~1의 값. 1이란 의미는 false positive가 0. 높을 수록 좋음
  - false postive가 false negative보다 더 크게 문제되는 경우, 다르게 말해서, 양성 예측은 정확해야 하는 경우
    - 예: 상환(상환1, 연체0)으로 예측한 대출이 정확한게 중요함(예를 들기위해 상환을 postive로 놓았지만, negative로 설정하는게 더 좋음)

### Recall : 재현율. 실양성 중 진양성을 재현한 비율
  - true positive / (true positive + false negative)
  - TPR(true positive rate), Sensitivity 라고도 함
  - (실제 양성을) 재현 하는것. 실제 양성인 케이스들을 양성으로 재현할 확율
  - 0~1의 값. 1이란 의미는 false negative가 0. 높을 수록 좋음
  - false negative가 false positive보다 더 크게 문제되는 경우. 다르게 말해서, 실제 양성들은 모두 맞춰야 하는데, 실제 양성 중 얼마나 맞추는지를 보는 것
    - 예: 트랜젝션 여부를 잘못 탐지하여, false negative한 경우가 많으면 더 크리티컬 한 경우에 recall값을 봐야 함
    - 예: 실제 연체(연체 1, 상환 0)한 대출을 다 맞추는게 중요.
    - 예: 실제 코로나 양성을 다 맞추는게 중요.
  - 실제 positive한 얘들의 정밀도를 구하는 것


### Precision vs Recall
  - 어떤 경우를 양성으로 놓느냐에 따라, Precision이나 Recall이 더 중요한지 다름
  - Precision은 양성 예측한 값이 모두 정확한게 더 중요한 경우 확인
  - Recall은 실제 양성을 모두 재현하는게 더 중요한 경우 확인


### F1 score : Precision과 Recall의 조화 평균
  - 조화 평균을 쓰는이유는? https://wikidocs.net/23088
    - 어떤 평균을 쓸지는 해당 값이 무엇인가에 따라 다르다
    - 산술 평균 : 합의 평균
    - 기하 평균 : 곱의 평균 
      - (사용 예: 연 평균 증가율. 증가 비율은 합의 평균으로 구할 수 없다.)
    - 조화 평균 : 2ab/(a+b)
      - 갈 때 10m/s, 올때 20m/s 로 주행하였다. 평균 속력
      - 갈 때와 올때 걸린 시간이 다르므로, 시간을 감안하여 평균 속력을 구해야 함.
      - 속력처럼, 분모의 값이 다른 경우에, 조화 평균을 사용하는 듯.
      - precision은 분모가 양성 예측 수, recall은 분모가 실제 양성 수로 분모가 다름


### Accuracy vs F1 score
  - True negative는 일반적으로 별로 신경 안 쓰고, positive가 많을 때 문제가 됨.
    - 예: 코로나 확진자 수가 많다
    - 예: 연체 수가 많다.
  - 그래서, true negative를 제외한 score가 F1 score



### TPR, FPR
- True Positive Rate = TP / (TP + FN) (recall) 실 양성 중 진 양성의 비율
- False Negative Rate = FN / (TP + FN) : 실제 양성 중 위음성의 비율. 1 - TPR = FNR
- True Negative Rate = TN / (TN + FP) : 실 음성 중 진음성 비율
- False Positive Rate = FP / (TN + FP) : 실 음성 중 위양성의 비율


### ROC, AUC
- Receiver Operator Characteristic
- threshold 0~1 사이 변화에 따른, TPR, FPR사이의 그래프
- threshold가 0이면, 전부 양성 예측하여, TPR은 좋아지고, FPR은 나빠짐
- threshold가 1이면, 전부 음성 예측하여, TPR은 나빠지고, FPR은 좋아짐

### AUROC
- AUC곡선의 밑의 넓이
- 무작위일 경우, 0.5. 0.7 미만의 경우 차선(Sub-optimal)으로 고려할 수 있는 정도이며, 0.7~0.8은 좋은(Good) 정도, 0.8 이상은 훌륭한(Excellent) 정도로 봅니다

### 대출 성능 지표
- 대출은 시간이 흐름에 따라, 데이터의 편향이 지속적으로 발생하게 됨(연체로 예측된 경우 대출을 안주기 때문에, TN, FN 의 데이터만 지속적으로 쌓이고, 점차 범위가 TN으로 좁아짐)
  - 따라서, recall이나 precision은 정답을 알 수 없기때문에, 의미가 없는 수치
- 연체율 = 연체 수 / 전체 대출 수 =  false negative / (true negative + false negative)
- 승인율 = 상환 예측 수 / 전체 신청 수 = (TN + FN) / (TN + FN + TP + FP)
  - TP, FP에 대한 데이터가 부족한데, 승인율을 올리는 것은 FP중에 negative가 있을 가능성을 고려하여, 위험을 감수하고, 매출을 올리기 위한 시도
  - threshold를 낮춰서 승인율을 올렸을 때, 파악되지 않은 성향의 대출이 나가게 되고, 여기에 대해서는, 실제 피해를 겪어보면서, 지속적으로 학습해서 보완할 수 밖에 없음



### Gain Chart
- cutoff 에 따라 10개의 decile로 나눈다.
- 100명 중 80명이 상환을 했다면,
- random으로 대출 승인시 50% 확률이라면,, 10% cutoff는 8명 승인 되고,
- model에 따라 승인시, 10% cutoff에 더 많은 사람이 승인 받을 수 있음을 보여줌.
- 그래서, cutoff에 따른 상환율을 그래프로 쉽게 보여 줌.
- y축은 누적 상환수, x축은 0~1 사이의 각 cut off.
- (x, y)는 특정 cutoff 에 대한 상환 수를 보여줌.
- x: decile, y: cumulative numer of positive observations upto declie
- gain: y/ total number of positive observations : 1 decile에서 100% 가 나옴