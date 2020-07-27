import unittest

from src.bicimad.constants.bikes_constants import *
import src.bicimad.constants.paths
from src.bicimad.operations.cleaning_operations import transform_types, remove_outliers_travel_time, clean_date, UPPER_QUANTILE, LOWER_QUANTILE
from src.general.operations.dataframe_operations import load_dataframe


class CleaningOperationsTest(unittest.TestCase):

    PATH_BIKES = '../../../' + src.bicimad.constants.paths.path_bikes_raw
    df_bikes = load_dataframe(PATH_BIKES)

    def test_clean_stations(self):
        # TODO
        pass

    def test_transform_types(self):
        # TODO
        pass

    def test_remove_outliers_travel_time(self):
        # TODO improve test
        expected_shape = 0
        df_bikes = transform_types(self.df_bikes)
        upper_limit = df_bikes[bikes_col_travel_time].quantile(UPPER_QUANTILE)
        lower_limit = df_bikes[bikes_col_travel_time].quantile(LOWER_QUANTILE)
        df_bikes_clean = remove_outliers_travel_time(df_bikes)
        self.assertEqual(df_bikes_clean[(df_bikes_clean[bikes_col_travel_time] > upper_limit) &
                                           (df_bikes_clean[bikes_col_travel_time] < lower_limit)].shape[0],
                         expected_shape)

    def test_clean_date(self):
        # TODO improve test
        df_bikes = transform_types(self.df_bikes)
        df_bikes_clean = clean_date(df_bikes)
        self.assertIn(bikes_col_day_of_week, df_bikes_clean.columns)
        self.assertIn(bikes_col_day, df_bikes_clean.columns)
        self.assertIn(bikes_col_month, df_bikes_clean.columns)

    def test_filter_out_employees(self):
        # TODO
        pass
