import unittest

from bicimad.constants.model import TEST_SIZE
from bicimad.constants.paths import PATH_DATASET
from bicimad.modeling.utils import split_data
from general.operations.dataframe_operations import load_dataframe_from_csv


class ModelingUtilsTest(unittest.TestCase):
    PATH_DATASET_HOURLY = '../../../' + PATH_DATASET.get('hourly')
    PATH_DATASET_DAILY = '../../../' + PATH_DATASET.get('daily')
    df_hourly = load_dataframe_from_csv(PATH_DATASET_HOURLY)
    df_daily = load_dataframe_from_csv(PATH_DATASET_DAILY)

    def test_split_data(self):
        print(self.df_hourly.dtypes)
        train, test = split_data(self.df_hourly, test_size=TEST_SIZE)
        expected_size = 524
        self.assertEqual(expected_size, train.shape[0])

