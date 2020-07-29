import unittest
import numpy as np
from bicimad.constants.model import MODEL_FEATURES
from bicimad.modeling.utils import prepare_data

from bicimad.modeling.xgboost import xgboost_model

from general.operations.dataframe_operations import load_dataframe_from_csv
from bicimad.constants.paths import PATH_DATASET
import xgboost as xgb

class XGBoostTest(unittest.TestCase):
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    PATH_DATASET_HOURLY = '../../../' + PATH_DATASET.get('hourly')
    df_hourly = load_dataframe_from_csv(PATH_DATASET_HOURLY)

