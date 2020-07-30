import unittest
import numpy as np

from bicimad.constants.rides import COL_BIKES_DATE, COL_BIKES_RIDES, COL_BIKES_HOUR
from bicimad.constants.weather import COL_WEATHER_DATE, COL_WEATHER_RAIN, COL_WEATHER_TEMP_MEAN, COL_WEATHER_WIND_MEAN, COL_WEATHER_TEMP_HOURLY
from bicimad.constants.paths import PATH_BIKES_CLEAN, PATH_AEMET_PER_DAY
from general.operations.dataframe_operations import load_dataframe_from_csv, load_dataframe_from_json
from bicimad.operations.aggregation import preprocess_rides_per_day, preprocess_rides_per_hour, add_weather_data_per_day, prepare_daily_data, \
    get_temperature_model, get_temperature_simple, get_hourly_weather, add_mean_rides_for_day

#T ODO tests are only valid for current data. Create data folder inside test folder to provide test reproducibility.


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

    def test_preprocess_rides_per_hour(self):
        df_rides_per_hour = preprocess_rides_per_hour(self.df_bikes)
        expected_size = 656
        self.assertIn(COL_BIKES_RIDES, df_rides_per_hour.columns)
        self.assertIn(COL_BIKES_HOUR, df_rides_per_hour.columns)
        self.assertEqual(df_rides_per_hour.shape[0], expected_size)

    def test_add_mean_rides_for_day(self):
        df_rides_per_day = preprocess_rides_per_day(self.df_bikes)
        dd = add_mean_rides_for_day(df_rides_per_day)
        self.assertEqual(0, 0)

    def test_add_weather_data_per_day(self):
        df_rides_per_day = preprocess_rides_per_day(self.df_bikes)
        df_with_weather = add_weather_data_per_day(df_rides_per_day, self.df_weather)
        self.assertIn(COL_WEATHER_RAIN, df_with_weather.columns)
        self.assertIn(COL_WEATHER_TEMP_MEAN, df_with_weather.columns)
        self.assertIn(COL_WEATHER_WIND_MEAN, df_with_weather.columns)

    def test_prepare_daily_data(self):
        dataset = prepare_daily_data(self.df_bikes, self.df_weather)
        self.assertNotIn(COL_BIKES_DATE, dataset.columns)

    def test_get_temperature_model(self):
        model = get_temperature_model(20, 24, 10, 12)
        print(model.predict(np.array(11.0).reshape(1, -1)))
        self.assertAlmostEqual(model.coef_[0], 2.0)
        self.assertAlmostEqual(model.intercept_, 0.0)

    def test_get_temperature_simple(self):
        expected_value = 20.0
        self.assertEqual(expected_value, get_temperature_simple(7, 20, 15, 35, 6, 14))

    def test_get_hourly_weather(self):
        df_rides_per_hour = preprocess_rides_per_hour(self.df_bikes)
        df_with_weather = add_weather_data_per_day(df_rides_per_hour, self.df_weather)
        df_with_weather_hourly = get_hourly_weather(df_with_weather)
        self.assertIn(COL_WEATHER_TEMP_HOURLY, df_with_weather_hourly.columns)