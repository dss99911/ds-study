import tensorflow as tf
from tensorflow.keras import *
from tensorflow.keras import layers
from tensorflow.keras import models
import pandas as pd
import numpy as np

df = pd.read_csv("data/gpascore.csv")
df = df.dropna()
features = df.drop(columns=['admit']).values
label = df["admit"].values
label_onehotencoding = pd.get_dummies(df['admit']).values  # onehot encoding형식으로 바꿔줌
#%%

# 처음 : 피쳐가 3개라서 3
# 마지막 : label 컬럼 갯수가 1개라서 마지막이 1.
#   - label을 onehot-encoding으로 표시하면, 컬럼이 class갯수가 만큼 생기고, 컬럼의 수로 설정해주면 됨.
#   - 3개 이상의 class의 경우, activation function으로 softmax를 사용함.
model = models.Sequential([
    layers.Dense(3, activation="tanh"),  # activation : sigmoid, tanh, relu, softmax, leakyRelu
    layers.Dense(6, activation="tanh"),  # hidden layer, node갯수가 128개
    layers.Dense(1, activation="sigmoid"),  # 결과 값이 하나 이므로 1, 0~1사이의 확률 값을 리턴하고 싶으면, sigmoid설정
])
# - sigmoid : 출력 범위 0~1 사이. 결과 값이 하나일 경우, 0~1사이의 확률 값을 리턴하고 싶은 경우 사용.
# - tanh : 출력 범위는 -1에서 1사이라는 점입니다. Sigmoid와 비교하여 tanh와는 출력 범위가 더 넓고 경사면이 큰 범위가 더 크기 때문에 더 빠르게 수렴하여 학습하는 특성
# - Softmax : 3-class 이상의 classification을 목적으로 하는 딥러닝 모델의 출력층에서 일반적으로 쓰이는 활성화 함수(activation function)
# - relu : 요즘에는 이걸 많이 쓴다고 함

model.compile(optimizer="adam",  # optimizer : adam, adagrad, adadelta, rmsprop, sgd
              loss="binary_crossentropy",  # 손실함수, 이진분류의 경우, binary_crossentropy
              metrics=["accuracy"]
              )

model.fit(features, label, epochs=1000)

feature_predict = [
    [750, 3.70, 3],
    [400, 2.2, 1]
]
label_predict = model.predict(feature_predict)