# Deep learning

## Perceptron

### Single perceptron
- 딥러닝의 시작점은 Perceptron
- w*x + b 의 합으로 시작
- 약간 linear regression과 비슷한 것 같음 각 피쳐별 가중치를 설정하는 방식


### Multiple Perceptron
- single perceptron은 XOR 처럼 linear하지 않은 경우에 한계가 있고, 그래서, 다중 퍼셉트론이 나옴.

#### 방식
- 피쳐값과 예측값 사이에, 여러 hidden layer를 추가함
- 히든 레이어의 노드 수는 임의로 정할 수 있고, 노드별로 값이 존재
- 노드의 값은 앞 레이어의 값에 가중치를 곱한 합에 b를 더한 후, activation function으로 값을 정재한 값임
- 히든 레이어 종류, 레이어의 노드 수, activation함수, 경사하강에 쓰는 optimizer, 손실함수 등을 설정해주면, 알아서 w와 b등을 설정해줌

#### 학습 로직
- W, b를 초기화 함(W는 랜덤값, b는 0)
- 순전파(forward propagation)로 예측 Y값 구함
  - 다중 퍼셉트론을 통해, 예측값을 구하는 것
  - W*x의 합 + b를 한 후, activation function으로 값을 정제(tanh, sigmoid, softmax, relu등)
- 손실함수로 손실값 구함
  - 순전파를 통해, 구한 예측값과 실제 값의 오차인 손실값을 손실함수로 구함
  - classification의 경우, logloss를 사용함
- 경사하강법으로 W, b를 수정
  - learning_rate만큼 W, b를 바꿔줌
  - optimizer를 잘 설정해줘야 함

#### 효과
- 다중 레이어로 바꿈으로써, linear하지 않고, 각 피쳐가 독립적이지 않고, 의존성이 있는 경우에 대해서 구할 수 있음.
- Decision, regression tree 도 각 피쳐가 독립적이지 않을 때, 사용하는데
- 단순히 피쳐들 사이의 의존성을 찾는게 아니라, 피쳐들의 결합을 토대로 새로운 정보를 만들어 내고, 그 정보를 토대로 가중치도 만들어 내기 때문에,
- Decision, regression tree 보다 더 복잡한 케이스(이미지 분류, 자연어 처리등 비정형 데이터) 학습 가능

### 경사 하강법
- 손실함수로 구한 손실값을 최소화 하는 w,b등 매개변수를 구하는 것으로 여러 optimizer가 있음

#### 손실함수
- 손실함수는 예측값과 실제값의 오차의 합을 구하는 것인데, 오차가 음수, 양수 모두 가능하므로 제곱을 해줌
- 이진 분류의 경우, binary_crossentropy, logloss 라는 공식 사용

#### optimizer
- learning rate가 크면, 최소 지점을 초과하여, 최소 지점에 가기 어려울 수도 있을 듯
- learning rate가 작으면, 필요한 하강횟수가 많아져서, 학습 속도가 느려짐
- 매개변수와 손실 값 사이의 그래프가 일정하지 않을 경우, 더 작은 손실값이 가능하더라도, 못 찾는 경우가 있으므로, learning rate 및 optimizer종류를 잘 설정할 필요가 있음(일반적으로 adam을 많이 쓴다고 함)
- 학습시간을 고려하여, 처음에는 0.1로 시도해보고, 그 이후 0.01, 0.001 순으로 시도, learning rate schedule기법이라는게 있음

## CNN
- 이미지에서 사용한다는 것 같음


## Recurrent Neural Networks
- 자연어 처리할 때 씀
- LSTM등과 사용한다고 함.
- hidden unit이 자신을 호출하는 recurrent한 구조라고 함
- 시계열 처리하기 위해 탄생. 기존 신경망은 앞으로만 전진하는데 반해, rnn은 자기 자신을 참조
- 다중 퍼셉트론의 경우, 같은 레이어의 노드들은 독립적인데(앞단의 레이어의 노드들은 서로 연관이 가능), RNN의 경우, 같은 레이어의, 노드들이 서로 연관됨.

### LSTM
- https://colah.github.io/posts/2015-08-Understanding-LSTMs/

- Vanishing gradient probelm : RNN에서 같은 레이어의 노드들 끼리 연결되는 값은 동일 값. 해당 값이 노드들을 거칠수록 곱해지므로, 약간만 작아도, 값이 점차 작아지고, 약간만 커도, 엄청 커지는 문제가 있음
- 이 문제를 해결하기 위해서, LSTM이 나옴
- 옛날 정보를 기억할지, 잊어버릴지 조절


### Hidden Markov model

#### Markov model
- markov 가정 : 시간 t에서 관측은 가장 최근 r개의 관측에만 의존한다
사용 사례
  - 염기서열에서 유전자 찾기
  - 주어진 단어의 품사 추측
- 은닉 상태인 y를 예측할 때, 비터비(viterbi) 알고리즘 사용
  - 가장 가능성 높은 path를 결정하는 로직
- 학습시, 각 상태별 전이비율, 초기비율, 출력비율을 구하고, 예측시 전이확률, 초기확률, 출력확률을 구하여, 예측 상태값을 구함

### RNN 성능 개선 방법
- GRU 알고리즘
- 재귀적 드랍아웃
- 다적층 방법(유닛 수, 레이어수 늘리기)
- 양방향 RNN