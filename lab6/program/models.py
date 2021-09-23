import numpy as np
import random

import torch
import torch.nn as nn
import torch.nn.functional as F

# TODO(Lab-02): Complete the network model.
class PolicyNet(nn.Module):
    def __init__(self):
        super(PolicyNet, self).__init__()
        self.fc1 = nn.Linear(23, 512)
        self.fc2 = nn.Linear(512, 512)
        self.fc3 = nn.Linear(512, 512)
        self.action = nn.Linear(512, 2)
        self.tanh = nn.Tanh()
        self.relu = nn.ReLU()

    def forward(self, s):
        x = self.relu(self.fc1(s))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.tanh(self.action(x))
        return x


class QNet(nn.Module):
    def __init__(self):
        super(QNet, self).__init__()
        self.fc1 = nn.Linear(23, 512)
        self.fc2 = nn.Linear(514, 512)
        self.fc3 = nn.Linear(512, 512)
        self.action = nn.Linear(512, 1)
        self.relu = nn.ReLU()
    
    def forward(self, s, a):
        x = self.relu(self.fc1(s))
        x = torch.cat((x, a), 1)
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.action(x)
        return x


        
