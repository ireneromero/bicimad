import unittest

from general.operations.dataframe_operations import load_dataframe_from_csv
from bicimad.constants.paths import PATH_DATASET


class XGBoostTest(unittest.TestCase):
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    PATH_DATASET_HOURLY = '../../../' + PATH_DATASET.get('hourly')
    df_hourly = load_dataframe_from_csv(PATH_DATASET_HOURLY)

