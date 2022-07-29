import torch
from torch_module import NeuralNetwork

# process of adjusting model parameters to reduce model error in each training step

learning_rate = 1e-3
batch_size = 64
epochs = 5

model = NeuralNetwork()

# Stochastic Gradient Descent
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
torch.optim.adam
torch.optim.rmsprop

optimizer.zero_grad()  # grad to zero
# loss.backward()  # computing grad
optimizer.step()  # reflect grad
