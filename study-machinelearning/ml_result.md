## F1 Score
  - https://blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221531940245

### Precision : positive예측(true positive + false positive) 중 true positive의 비율
  - 높을 수록 좋음
  - 0~1의 값. 1이란 의미는 false positive가 0
  - positve로 예측한 얘들의 정밀도

### Recall : 실제 positive(true positive + false negative) 중 true positive의 비율
  - 높을 수록 좋음
  - 0~1의 값. 1이란 의미는 false negative가 0
  - 트랜젝션 여부를 잘못 탐지하여, false negative한 경우가 많으면 더 크리티컬 한 경우에 recall값을 봐야 함
  - 실제 positive한 얘들의 정밀도를 구하는 것

### F1 score : Precision과 Recall의 조화 평균
  - 조화 평균을 쓰는이유는? https://wikidocs.net/23088
    - 어떤 평균을 쓸지는 해당 값이 무엇인가에 따라 다르다
    - 산술 평균 : 합의 평균
    - 기하 평균 : 곱의 평균 
      - (사용 예: 연 평균 증가율. 증가 비율은 합의 평균으로 구할 수 없다.)
    - 조화 평균 : 
      - 갈 때 10m/s, 올때 20m/s 로 주행하였다. 평균 속력
      - 갈 때와 올때 걸린 시간이 다르므로, 시간을 감안하여 평균 속력을 구해야 함.
      - 속력처럼, 분모의 값이 다른 경우에, 조화 평균을 사용하는 듯.
      - precision과 recall도 분모가 다름.
        - 