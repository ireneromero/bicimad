import unittest

from src.bicimad.constants.bikes_constants import *
from src.bicimad.constants.weather_constants import *
from src.bicimad.constants.paths import *
from src.bicimad.operations.cleaning_operations import transform_types_bikes, remove_outliers_travel_time, clean_date_bikes, UPPER_QUANTILE, LOWER_QUANTILE
from src.general.operations.dataframe_operations import load_dataframe_from_csv, load_dataframe_from_json
from src.bicimad.operations.aggregation_operations import preprocess_rides_per_day, add_weather_data_per_day, prepare_daily_data

#TODO tests are only valid for current data. Create data folder inside test folder to provide test reproducibility.

class AggregationOperationsTest(unittest.TestCase):

    PATH_BIKES_CLEAN = '../../../' + PATH_BIKES_CLEAN
    PATH_WEATHER = '../../../' + PATH_AEMET_PER_DAY
    df_bikes = load_dataframe_from_csv(PATH_BIKES_CLEAN, parse_dates=[COL_BIKES_DATE])
    df_weather = load_dataframe_from_json(PATH_WEATHER, parse_dates=[COL_WEATHER_DATE])

    def test_preprocess_rides_per_day(self):
        df_rides_per_day = preprocess_rides_per_day(self.df_bikes)
        expected_size = 28
        self.assertEqual(df_rides_per_day.shape[0], expected_size)
        self.assertIn(COL_BIKES_RIDES, df_rides_per_day.columns)

    def test_add_weather_data_per_day(self):
        df_rides_per_day = preprocess_rides_per_day(self.df_bikes)
        df_with_weather = add_weather_data_per_day(df_rides_per_day, self.df_weather)
        self.assertIn(COL_WEATHER_RAIN, df_with_weather.columns)
        self.assertIn(COL_WEATHER_TEMP_MEAN, df_with_weather.columns)
        self.assertIn(COL_WEATHER_WIND_MEAN, df_with_weather.columns)

    def test_prepare_daily_data(self):
        dataset = prepare_daily_data(self.df_bikes, self.df_weather)
        self.assertNotIn(COL_BIKES_DATE, dataset.columns)

