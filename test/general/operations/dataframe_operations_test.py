import unittest
from src.general.operations.dataframe_operations import load_dataframe, save_dataframe
import src.bicimad.constants.paths

class DataFrameOperationsTest(unittest.TestCase):

    PATH_BIKES = '../../../' + src.bicimad.constants.paths.path_bikes_raw

    def test_load_dataframe(self):
        df_bikes = load_dataframe(self.PATH_BIKES)
        expected_size = 398040
        self.assertEqual(df_bikes.shape[0], expected_size)
