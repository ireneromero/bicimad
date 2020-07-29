import torch
import torch.nn as nn
import torch.nn.functional as F
from bicimad.constants.paths import PATH_MODEL_DEEPLEARNING_MODEL
from pandas import DataFrame as DataFrame
from sklearn.metrics import mean_squared_error, r2_score

from bicimad.modeling.utils import prepare_data, split_data

from bicimad.constants.model_constants import FEATURES_DAILY, TARGET, HIDDEN_DIMENSION, TEST_SIZE, EPOCHS


class Net(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)

def create_net():
    # TODO implement other optimizers
    net = Net(len(FEATURES_DAILY), HIDDEN_DIMENSION, 1)
    optimizer = torch.optim.Adam(net.parameters(), lr = 0.01)
    loss_criterion = nn.MSELoss()
    return net, optimizer, loss_criterion

def prepare_data_for_deep_learning(df: DataFrame):

    # TODO add parameter to select between daily/hourly data
    # TODO check overfitting for overfitting using validation set
    # TODO scale data
    # TODO fix prepare_data and split_data to use them with this purpose
    df_train, df_test = prepare_data(df)
    df_train, df_val = split_data(df_train, TEST_SIZE)

    train_features_tensor = torch.tensor(df_train[FEATURES_DAILY].values).float()
    train_target_tensor = torch.tensor(df_train[TARGET].values).float()
    val_features_tensor = torch.tensor(df_val[FEATURES_DAILY].values).float()
    val_target_tensor = torch.tensor(df_val[TARGET].values).float()
    test_features_tensor = torch.tensor(df_test[FEATURES_DAILY].values).float()
    test_target_tensor = torch.tensor(df_test[TARGET].values).float()
    return train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor, test_features_tensor, test_target_tensor


def train_net(net, optimizer, loss_criterion, epochs, train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor):
    losses = []
    losses_val = []
    for i in range(epochs):
        predictions = net(train_features_tensor)
        loss = loss_criterion(predictions, train_target_tensor.view(-1, 1))
        losses.append(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        with torch.no_grad():
            predictions_val = net(val_features_tensor)
            loss_val = loss_criterion(predictions_val, val_target_tensor.view(-1, 1))
            losses_val.append(loss_val.item())

    return net, losses, losses_val

def evaluate_net(net, test_features_tensor, test_target_tensor, metrics=['r2']):
    metrics_result = {}
    with torch.no_grad():
        net.eval() # not necessary since no dropout layers
        predictions_test = net(test_features_tensor)
    if 'mse' in metrics:
        metrics_result['mse'] = mean_squared_error(test_target_tensor, predictions_test)
    if 'r2' in metrics: # if r2 negative, then it fits worse than a horizontal line
        metrics_result['r2'] = r2_score(test_target_tensor, predictions_test)
    return metrics_result


def deep_learning_model(dataset):
    train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor, test_features_tensor, test_target_tensor = prepare_data_for_deep_learning(dataset)
    net, optimizer, loss_criterion = create_net()
    net, losses, losses_val = train_net(net, optimizer, loss_criterion, EPOCHS, train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor)
    metrics = evaluate_net(net, test_features_tensor, test_target_tensor, metrics=['mse', 'r2'])
    return net, metrics

def save_model(net, path):
    torch.save(net.state_dict(), path)


