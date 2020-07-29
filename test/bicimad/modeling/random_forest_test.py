import unittest
import numpy as np
from bicimad.constants.model import FEATURES_DAILY

from general.operations.dataframe_operations import load_dataframe_from_csv
from bicimad.constants.paths import PATH_DATASET
from bicimad.modeling.random_forest import random_forest_model, random_forest_feature_importance


class RandomForestTest(unittest.TestCase):
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    def test_feature_importance(self):
        rf, metrics, ft_importance = random_forest_model(self.df_daily, feature_importance=True)
        print(ft_importance)
        self.assertEqual(0, 0)
