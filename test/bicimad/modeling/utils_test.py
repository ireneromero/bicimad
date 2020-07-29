import unittest
from sklearn.model_selection import train_test_split

from bicimad.constants.paths import PATH_DATASET
from bicimad.constants.model_constants import TEST_SIZE, CATEGORICAL_COLUMNS_DAILY

from bicimad.constants.bikes_constants import COL_BIKES_DATE
from general.operations.dataframe_operations import load_dataframe_from_csv

from bicimad.modeling.utils import split_data, encode_categorical

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

    def test_encode_categorical(self):
        # TODO
        df_daily_encoded = encode_categorical(self.df_daily, CATEGORICAL_COLUMNS_DAILY)
        #print(df_daily_encoded.columns)
        #self.assertEqual(0, 0)
        pass
