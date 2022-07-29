
import os
import pandas as pd
from torchvision import datasets
from torchvision.io import read_image
from torchvision.transforms import ToTensor, Lambda

#%% open data set
training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

#%% transform
ds = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,

    # feature image to tensor
    transform=ToTensor(),

    # label int to onehot encoding
    target_transform=Lambda(lambda y: torch.zeros(10, dtype=torch.float).scatter_(0, torch.tensor(y), value=1))
)

#%% custom dataset
# annotations_file처럼, 전체 학습데이터를 불러와도, 데이터가 크지 않고, 큰 데이터는 getitem에서 불러올 수 있으면 Dataset을 사용이 편리하다.
# 하지만, 텍스트 데이터가 여러 파일에 저장되어 있고, 파일마다 row갯수가 다른 경우, 전체 데이터를 불러오기 부담스럽다면, Dataset을 여러개 생성해서 로딩해야 하고, 불필요한 코드가 많아진다
class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label