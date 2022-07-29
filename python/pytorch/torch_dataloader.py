from torch.utils.data import DataLoader
from torchvision import datasets

training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

#%%
# shuffle reduce overfitting
train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)

for batch, (X, y) in enumerate(dataloader):
    print(batch, X, y)
    break

#%%

torch.zeros(10, dtype=torch.float).scatter_(0, torch.tensor(2), value=1)
