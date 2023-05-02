import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, filename):
        #Read CSV
        data = pd.read_csv(filename, header=None)
      
        #Split into features and labels 
        self.X = torch.tensor(data.iloc[:, :-1].values, dtype=torch.float32)
        self.y = torch.tensor(data.iloc[:, -1].values, dtype=torch.int8)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


#Datasets
train_dataset = MyDataset('datasets/training.csv')
test_dataset = MyDataset('datasets/testing.csv')

#save
torch.save(train_dataset, 'datasets/train_dataset.pt')
torch.save(test_dataset, 'datasets/test_dataset.pt')