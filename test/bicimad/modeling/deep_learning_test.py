import unittest

from bicimad.constants.paths import PATH_DATASET
from general.operations.dataframe_operations import load_dataframe_from_csv


class DeepLearningTest(unittest.TestCase):
    PATH_DATASET_HOURLY = '../../../' + PATH_DATASET.get('hourly')
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_hourly = load_dataframe_from_csv(PATH_DATASET_HOURLY)
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    def test_create_net(self):
        # TODO
        pass
