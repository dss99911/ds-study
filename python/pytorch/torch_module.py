import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torchvision.models as models

#%% pretraiend models
model = models.vgg16(pretrained=True)

#%% save
# use pickle
torch.save(model.state_dict(), 'model/model_weights.pth')

#%% load
# 모델 클래스 인스턴스 생성 후, state만 불러오는 방식.
model = models.vgg16() # we do not specify pretrained=True, i.e. do not load default weights
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()  # 2D 으로 변환(첫번째는 row 디멘션, 두번째는 피쳐 디멘션)

        #28*28 피쳐 -> 512 -> 10 output
        self.linear_relu_stack = nn.Sequential(  # container
            nn.Linear(28*28, 512),
            nn.ReLU(),  # activation 함수를 분리해서 사용함
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    # 이 함수를 정의 해야 함.
    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

model = NeuralNetwork().to(device)
print(model)

# show Weight, Bias
#   - weight: input에서 output으로 변환되는 가중치 tensor[output][input]
#   - bias: output에 값 변경을 주는 tensor[output]
for name, param in model.named_parameters():
    print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]} \n")

X = torch.rand(1, 28, 28, device=device)

# 모델 prediction
logits = model(X)
# 모델외부에서도 직접 호출 가능
pred_probab = nn.Softmax(dim=1)(logits)  # softmax로 각 output에 대한 확률. 전체를 합하면 1이 나옴

y_pred = pred_probab.argmax(1)  # dim=1, 가장 큰 값의 index 리턴
print(f"Predicted class: {y_pred}")


