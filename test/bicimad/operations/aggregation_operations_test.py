import unittest

from src.bicimad.constants.bikes_constants import *
from src.bicimad.constants.weather_constants import *
from src.bicimad.constants.paths import *
from src.bicimad.operations.cleaning_operations import transform_types_bikes, remove_outliers_travel_time, clean_date_bikes, UPPER_QUANTILE, LOWER_QUANTILE
from src.general.operations.dataframe_operations import load_dataframe_from_csv, load_dataframe_from_json
from src.bicimad.operations.aggregation_operations import preprocess_rides_per_day, add_weather_data_per_day

#TODO tests are only valid for current data. Create data folder inside test folder to provide test reproducibility.

class AggregationOperationsTest(unittest.TestCase):

    PATH_BIKES_CLEAN = '../../../' + path_bikes_clean
    PATH_WEATHER = '../../../' + path_aemet_per_day
    df_bikes = load_dataframe_from_csv(PATH_BIKES_CLEAN, parse_dates=[COL_BIKES_DATE])
    df_weather = load_dataframe_from_json(PATH_WEATHER, parse_dates=[COL_WEATHER_DATE])

    def test_preprocess_rides_per_day(self):
        df_rides_per_day = preprocess_rides_per_day(self.df_bikes)
        expected_shape = (28, 2)
        self.assertEqual(df_rides_per_day.shape, expected_shape)

    def test_add_weather_data_per_day(self):
        df_rides_per_day = preprocess_rides_per_day(self.df_bikes)
        df_with_weather = add_weather_data_per_day(df_rides_per_day, self.df_weather)
        print(df_with_weather.dtypes)
        self.assertEqual(0, 0)