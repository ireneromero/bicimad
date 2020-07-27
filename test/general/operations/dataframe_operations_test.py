import unittest
from src.general.operations.dataframe_operations import load_dataframe_from_csv, load_dataframe_from_json
from src.bicimad.constants.paths import *
from src.bicimad.constants.bikes_constants import *
from src.bicimad.constants.weather_constants import *

class DataFrameOperationsTest(unittest.TestCase):

    PATH_BIKES = '../../../' + PATH_BIKES_RAW
    PATH_WEATHER = '../../../' + PATH_AEMET_PER_DAY
    PATH_BIKES_CLEAN = '../../../' + PATH_BIKES_CLEAN

    def test_load_dataframe_from_csv(self):
        df_bikes = load_dataframe_from_csv(self.PATH_BIKES)
        expected_size = 398040 #TODO use tuple
        self.assertEqual(df_bikes.shape[0], expected_size)

    def test_load_dataframe_from_csv_date(self):
        df_bikes = load_dataframe_from_csv(self.PATH_BIKES_CLEAN, parse_dates=[COL_BIKES_DATE])
        expected_size = 398040  # TODO use tuple
        self.assertEqual(df_bikes.shape[0], expected_size)

    def test_load_dataframe_from_json(self):
        df_weather = load_dataframe_from_json(self.PATH_WEATHER)
        expected_shape = (28, 19)
        self.assertEqual(df_weather.shape, expected_shape)

    def test_load_dataframe_from_json_date(self):
        df_weather = load_dataframe_from_json(self.PATH_WEATHER, parse_dates=[COL_WEATHER_DATE])
        expected_shape = (28, 19)
        self.assertEqual(df_weather.shape, expected_shape)