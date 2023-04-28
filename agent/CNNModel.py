import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Define the CNN model
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(2, 16, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2)
        self.fc1 = nn.Linear(32, 64)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        x = self.tanh(x)
        return x

def convert_to_state_input(board):
    ''' Translate the board into state '''
    
    if len(board.shape) < 3:
        print(board)
        board = board.reshape([2, 7, 7])
        
    new_board = np.zeros([2,7,7], dtype=int)

    # Channel 1: represents the positions of tokens
    set_oppo = lambda x: -1 if x > 0 else 0
    set_curr = lambda x: 1 if x > 0 else 0
    oppo = np.array([[set_oppo(e) for e in r] for r in board[1]])
    curr = np.array([[set_curr(e) for e in r] for r in board[0]])
    new_board[0] = oppo + curr

    # Channel 2: represents the power of all tokens
    add = board[0] + board[1]
    new_board[1] = np.copy(add)
    
    return new_board