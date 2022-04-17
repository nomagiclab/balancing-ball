from neural_networks.models import AbstractNet
import torch.nn as nn
import torch
import pickle
import time
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List


class CSVDataset(Dataset):
    #TODO: ustalic delimiter
    def __init__(self, csv_path: Path, x_indicies: List[int], y_indicies: List[int], delimiter: str = ',') -> None:
        super().__init__()
        self.data = np.genfromtxt(csv_path, delimiter=delimiter)
        self.x = torch.from_numpy(self.data[:, x_indicies]).float()
        self.y = torch.from_numpy(self.data[:, y_indicies]).float()
        self.size = self.data.shape[0]
    
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

    def __len__(self):
        return self.size


def create_dataloader(dataset: Dataset, batch_size: int) -> DataLoader:
    #TODO: shuffle=True? num_workes=>1? other args
    return DataLoader(dataset, batch_size=batch_size)

def train(net: nn.Module, dataloader_train, dataloader_test, optim, loss_function, epochs, eval_gap):
    for epoch in range(1, epochs + 1):
        if epoch % eval_gap == 0:
            net.eval()
            total_test_loss = 0
            for input, labels in dataloader_test:
                out = net(input)
                loss = loss_function(out, labels)
                total_test_loss += torch.sum(loss).item()
            print("AVG LOSS ON TEST SET:", total_test_loss/len(dataloader_test.dataset))

        net.train()
        total_train_loss = 0
        for input, labels in dataloader_train:
            optim.zero_grad()

            out = net(input)
            loss = loss_function(out, labels)
            total_train_loss += torch.sum(loss).item()
            loss.backward()
            optim.step()
        print("AVG LOSS ON TRAIN SET:", total_train_loss/len(dataloader_train.dataset))




def pickle_net(net: AbstractNet, path: Path, suffix: str = ""):
    path = Path(path)
    filehandler = open(path / (net.get_name() + suffix + str(time.time())), "wb")
    pickle.dump(net, filehandler)
    filehandler.close()