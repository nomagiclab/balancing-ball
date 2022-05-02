import torch.nn as nn
from typing import List
from abc import ABC


class AbstractNet(ABC):
    def __init__(self, *args, **kwargs):
        if "name" not in kwargs:
            raise "Net's constructor needs 'name' argument"
        self.name = kwargs["name"]

    def get_name(self) -> str:
        return self.name


class MLP(nn.Module, AbstractNet):
    def __init__(self, name: str, sizes: List[int]):
        AbstractNet.__init__(self, name=name)
        nn.Module.__init__(self)
        self.mod_list = nn.ModuleList()
        for i in range(len(sizes) - 1):
            self.mod_list.append(nn.Linear(sizes[i], sizes[i + 1]))
            if i + 1 != len(sizes):
                self.mod_list.append(nn.ReLU())

    def forward(self, x):
        for module in self.mod_list:
            x = module(x)
        return x
