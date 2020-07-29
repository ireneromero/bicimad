import unittest
import torch

from bicimad.modeling.deep_learning import create_net, train_net, prepare_data_for_deep_learning, evaluate_net
from sklearn.model_selection import train_test_split

from bicimad.constants.paths import PATH_DATASET
from bicimad.constants.model import TEST_SIZE, CATEGORICAL_COLUMNS_DAILY, EPOCHS

from bicimad.constants.rides import COL_BIKES_DATE
from general.operations.dataframe_operations import load_dataframe_from_csv

from bicimad.modeling.utils import split_data, encode_categorical

class DeepLearningTest(unittest.TestCase):
    PATH_DATASET_HOURLY = '../../../' + PATH_DATASET.get('hourly')
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_hourly = load_dataframe_from_csv(PATH_DATASET_HOURLY)
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    def test_create_net(self):
        # TODO
        # pass
        train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor, test_features_tensor, test_target_tensor = prepare_data_for_deep_learning(self.df_daily)
        net, optimizer, loss_criterion = create_net()
        net, losses, losses_val = train_net(net, optimizer, loss_criterion, EPOCHS, train_features_tensor, train_target_tensor, val_features_tensor, val_target_tensor)
        evaluate_net(net, test_features_tensor, test_target_tensor)
        print(test_features_tensor[0])
        print(test_target_tensor[0])
        print(net(test_features_tensor[0]))
        #self.assertAlmostEqual(net(data_to_test).item(), prediction_expected_real)
        #self.assertEqual(0, 0)
