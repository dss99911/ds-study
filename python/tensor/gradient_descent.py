import tensorflow as tf
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.optimizers
# 경사 하강법(Gradient descent) 에 대한 이해하기
#   - 손실함수를 토대로, 손실을 최소화 하는 매개변수를 구하는 것

# foot_size = height * a + b 라는 식에서 a와 b 구허기

height = 180
foot_size = 260

a = tf.Variable(0.1)
b = tf.Variable(0.1)

def loss_func():
    # real value - estimated value
    #   - 손실함수는 예측값과 실제값의 오차의 합을 구하는 것인데, 오차가 음수, 양수 모두 가능하므로 제곱을 해줌
    #   - 이진 분류의 경우, logloss, binary_crossentropy 라는 복잡한 공식 사용
    estimated = height * a + b
    return tf.square(foot_size - estimated)

optimizer = Adam(learning_rate=0.1)
# learning_rate : able to omit, 경사 하강법에서, 하강 정도의 비율.
#   - learning rate가 크면, 최소 지점을 초과하여, 최소 지점에 가기 어려울 수도 있을 듯
#   - learning rate가 작으면, 필요한 하강횟수가 많아져서, 학습 속도가 느려짐
#   - 매개변수와 손실 값 사이의 그래프가 일정하지 않을 경우, 더 작은 손실값이 가능하더라도, 못 찾는 경우가 있으므로, learning rate 및 optimizer종류를 잘 설정할 필요가 있음(일반적으로 adam을 많이 쓴다고 함)

for i in range(300):
    optimizer.minimize(loss=loss_func, var_list=[a, b])
    print(a.numpy(), b.numpy())
#%%

