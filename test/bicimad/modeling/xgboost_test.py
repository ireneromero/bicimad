import unittest
import numpy as np
from bicimad.constants.model import FEATURES_DAILY, TARGET
from bicimad.modeling.utils import prepare_data
from bicimad.modeling.xgboost import xgboost_model

from general.operations.dataframe_operations import load_dataframe_from_csv
from bicimad.constants.paths import PATH_DATASET
from bicimad.modeling.random_forest import random_forest_model, random_forest_feature_importance
import xgboost as xgb

class XGBoostTest(unittest.TestCase):
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    def test_feature_importance(self):
        dataset_train, dataset_test = prepare_data(self.df_daily)
        xgbmodel, metrics = xgboost_model(self.df_daily)
        print(metrics)
        self.assertEqual(0, 0)
