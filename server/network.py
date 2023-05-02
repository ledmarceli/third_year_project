import torch
import torch.nn as nn

#Define neural network
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(5, 25)
        self.fc2 = nn.Linear(25, 50)  
        self.relu1 = nn.ReLU()
        self.fc3 = nn.Linear(50, 75)
        self.relu2 = nn.ReLU()
        self.fc4 = nn.Linear(75, 100)
        self.relu3 = nn.ReLU()
        self.fc5 = nn.Linear(100, 150)
        self.relu4 = nn.ReLU()
        self.fc6 = nn.Linear(150, 2)         
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        x = self.relu2(x)
        x = self.fc4(x)
        x = self.relu3(x)
        x = self.fc5(x)
        x = self.relu4(x)
        x = self.fc6(x)
        x = self.sigmoid(x)
        return x 

#Load the network with weights
def initialise_model():
    model = Net()
    state_dict = torch.load('model.pth', map_location=torch.device('cpu'))
    model.load_state_dict(state_dict)
    return model