import unittest
from sklearn.model_selection import train_test_split

from bicimad.constants.paths import PATH_DATASET
from bicimad.constants.model_constants import TEST_SIZE

from bicimad.constants.bikes_constants import COL_BIKES_DATE
from general.operations.dataframe_operations import load_dataframe_from_csv

from bicimad.modeling.utils import split_data

class ModelingUtilsTest(unittest.TestCase):
    PATH_DATASET_HOURLY = '../../../' + PATH_DATASET.get('hourly')
    df_hourly = load_dataframe_from_csv(PATH_DATASET_HOURLY, parse_dates=[COL_BIKES_DATE])

    def test_split_data(self):
        print(self.df_hourly.shape[0])
        tr, ts = split_data(self.df_hourly, test_size=0.2)
        #df_train, df_test = split_data(self.df_hourly, TEST_SIZE)
        print(tr.shape[0])
        self.assertEqual(0, 0)
