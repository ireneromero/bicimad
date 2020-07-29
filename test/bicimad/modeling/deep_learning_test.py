import unittest
import torch

from bicimad.modeling.deep_learning import create_net, train_net, prepare_data_for_deep_learning, evaluate_net
from sklearn.model_selection import train_test_split

from bicimad.constants.paths import PATH_DATASET
from bicimad.constants.model_constants import TEST_SIZE, CATEGORICAL_COLUMNS_DAILY, EPOCHS

from bicimad.constants.bikes_constants import COL_BIKES_DATE
from general.operations.dataframe_operations import load_dataframe_from_csv

from bicimad.modeling.utils import split_data, encode_categorical

class DeepLearningTest(unittest.TestCase):
    PATH_DATASET_HOURLY = '../../../' + PATH_DATASET.get('hourly')
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_hourly = load_dataframe_from_csv(PATH_DATASET_HOURLY)
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    def test_create_net(self):
        # TODO
        pass
        # train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor, test_features_tensor, test_target_tensor = prepare_data_for_deep_learning(self.df_daily)
        # net, optimizer, loss_criterion = create_net()
        # net, losses, losses_val = train_net(net, optimizer, loss_criterion, EPOCHS, train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor)
        # evaluate_net(net, test_features_tensor, test_target_tensor)
        # data_to_test = torch.tensor([1.0000e+00, 0.0000e+00, 1.4940e+04, 2.1000e+01, 1.5700e+01, 2.6400e+01,
        # 0.0000e+00, 3.0000e-01]).float()
        #prediction_expected = 10212
        #prediction_expected_real = 15339.3223
        #print(net(data_to_test))
        #self.assertAlmostEqual(net(data_to_test).item(), prediction_expected_real)
        #self.assertEqual(0, 0)
