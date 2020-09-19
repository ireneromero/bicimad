from pandas import DataFrame as DataFrame
import numpy as np
from sklearn.linear_model import LinearRegression

from bicimad.constants.rides import COL_BIKES_DATE, COL_BIKES_DAY_OF_WEEK, COL_BIKES_RIDES, COL_BIKES_HOUR, \
    DAYS_IN_WEEKEND, VALUE_WEEKEND_TRUE, VALUE_WEEKEND_FALSE, COL_BIKES_WEEKEND, COL_BIKES_RIDES_MEAN_WEEKDAY, \
    COL_BIKES_RIDES_MEAN_WEEKDAY_HOUR
from bicimad.constants.weather import COL_WEATHER_DATE, COL_WEATHER_HOUR_TEMP_MAX, COL_WEATHER_HOUR_TEMP_MIN, \
    COL_WEATHER_TEMP_MAX, COL_WEATHER_TEMP_MIN, COL_WEATHER_WIND_MEAN, COL_WEATHER_RAIN, COL_WEATHER_TEMP_MEAN, \
    SUNRISE_HOUR, SUNSET_HOUR, COL_WEATHER_RAIN_HOURLY, COL_WEATHER_WIND_HOURLY, COL_WEATHER_TEMP_HOURLY


def preprocess_rides_per_day(df: DataFrame) -> DataFrame:
    # this dataframe should have a date column (parsed as datetime)
    return df.groupby([COL_BIKES_DATE, COL_BIKES_DAY_OF_WEEK]).size().reset_index(name=COL_BIKES_RIDES)


def preprocess_rides_per_hour(df: DataFrame) -> DataFrame:
    return df.groupby([COL_BIKES_DATE, COL_BIKES_DAY_OF_WEEK, COL_BIKES_HOUR]).size().reset_index(name=COL_BIKES_RIDES)


def add_weekend(df: DataFrame) -> DataFrame:

    def day_of_week_to_weekend(row):
        if row[COL_BIKES_DAY_OF_WEEK] in DAYS_IN_WEEKEND:
            return VALUE_WEEKEND_TRUE
        return VALUE_WEEKEND_FALSE

    df[COL_BIKES_WEEKEND] = df.apply(lambda row: day_of_week_to_weekend(row), axis=1)
    return df


def add_mean_rides_for_day(df: DataFrame) -> DataFrame:
    mean_for_weekday = df.groupby(COL_BIKES_DAY_OF_WEEK)[COL_BIKES_RIDES].mean().to_dict()
    df[COL_BIKES_RIDES_MEAN_WEEKDAY] = df[COL_BIKES_DAY_OF_WEEK].map(mean_for_weekday)
    return df


def add_mean_rides_for_day_and_hour(df: DataFrame) -> DataFrame:
    mean_for_weekday_and_hour = df.groupby([COL_BIKES_DAY_OF_WEEK, COL_BIKES_HOUR])[COL_BIKES_RIDES].mean().to_dict()

    def add_mean_rides_for_day_and_hour_for_row(row):
        return mean_for_weekday_and_hour.get((row[COL_BIKES_DAY_OF_WEEK], row[COL_BIKES_HOUR]))

    df[COL_BIKES_RIDES_MEAN_WEEKDAY_HOUR] = df.apply(lambda row: add_mean_rides_for_day_and_hour_for_row(row), axis=1)
    return df


def add_weather_data_per_day(df: DataFrame, df_weather: DataFrame) -> DataFrame:
    return df.merge(df_weather[[COL_WEATHER_DATE, COL_WEATHER_TEMP_MEAN, COL_WEATHER_RAIN, COL_WEATHER_WIND_MEAN,
                                COL_WEATHER_HOUR_TEMP_MAX, COL_WEATHER_HOUR_TEMP_MIN, COL_WEATHER_TEMP_MAX, COL_WEATHER_TEMP_MIN]],
             how='left',
             left_on=COL_BIKES_DATE,
             right_on=COL_WEATHER_DATE)


def prepare_daily_data(df: DataFrame, df_weather: DataFrame) -> DataFrame:
    df_rides_per_day = preprocess_rides_per_day(df)
    df_rides_per_day = add_weekend(df_rides_per_day)
    df_rides_per_day = add_mean_rides_for_day(df_rides_per_day)
    df_daily = add_weather_data_per_day(df_rides_per_day, df_weather)
    return df_daily.drop([COL_BIKES_DATE, COL_WEATHER_HOUR_TEMP_MAX, COL_WEATHER_HOUR_TEMP_MIN], axis=1)


def get_temperature_model(temp_1: float, temp_2: float, hour_temp_1: int, hour_temp_2: int) -> LinearRegression:
    temps = np.array([temp_1, temp_2])
    hours = np.array([hour_temp_1, hour_temp_2]).reshape(-1, 1)
    model = LinearRegression()
    model.fit(hours, temps)
    return model


def get_temperature_with_model(row):
    # TODO
    # we need to have weather information for 31/08 and 1/10
    pass


def get_temperature_simple_per_row(row):
    return get_temperature_simple(row[COL_BIKES_HOUR],
                                  row[COL_WEATHER_TEMP_MEAN],
                                  row[COL_WEATHER_TEMP_MIN],
                                  row[COL_WEATHER_TEMP_MAX],
                                  row[COL_WEATHER_HOUR_TEMP_MIN],
                                  row[COL_WEATHER_HOUR_TEMP_MAX])


def get_temperature_simple(hour_to_predict: int, temp_mean: float, temp_min: float, temp_max: float, hour_temp_min: int, hour_temp_max: int) -> float:
    temp = 0.0
    if (hour_to_predict < hour_temp_max + 2) & (hour_to_predict > hour_temp_max - 2): # time around max temperature
        temp = temp_max
    elif (hour_to_predict < SUNRISE_HOUR) | (hour_to_predict > SUNSET_HOUR): # night
        temp = temp_min
    else: # rest of the day
        temp = temp_mean
    return temp


def get_hourly_weather(df: DataFrame) -> DataFrame:
    df[COL_WEATHER_RAIN_HOURLY] = df[COL_WEATHER_RAIN]
    df[COL_WEATHER_WIND_HOURLY] = df[COL_WEATHER_WIND_MEAN]
    df[COL_WEATHER_HOUR_TEMP_MIN] = df[COL_WEATHER_HOUR_TEMP_MIN].astype(str).str[:2].astype(int)
    df[COL_WEATHER_HOUR_TEMP_MAX] = df[COL_WEATHER_HOUR_TEMP_MAX].astype(str).str[:2].astype(int)
    df[COL_WEATHER_TEMP_HOURLY] = df.apply(lambda row: get_temperature_simple_per_row(row), axis=1)
    return df


def prepare_hourly_data(df: DataFrame, df_weather: DataFrame) -> DataFrame:
    df_rides_per_hour = preprocess_rides_per_hour(df)
    df_rides_per_hour = add_weekend(df_rides_per_hour)
    df_rides_per_hour = add_mean_rides_for_day_and_hour(df_rides_per_hour)
    df_hourly = add_weather_data_per_day(df_rides_per_hour, df_weather)
    return get_hourly_weather(df_hourly).drop([COL_BIKES_DATE,
                                               COL_WEATHER_TEMP_MEAN,
                                               COL_WEATHER_RAIN,
                                               COL_WEATHER_WIND_MEAN,
                                               COL_WEATHER_HOUR_TEMP_MIN,
                                               COL_WEATHER_HOUR_TEMP_MAX], axis=1)


# TODO test this code, not yet used
def get_temperature_simple_v2(hour_to_predict: int,
                              yesterday_temp_min_hour: int, yesterday_temp_min: float, yesterday_temp_max_hour: int,
                              yesterday_temp_max: float,
                              temp_min: float, temp_max: float, hour_temp_min: int, hour_temp_max: int,
                              tomorrow_temp_min_hour: int, tomorrow_temp_min: float, tomorrow_temp_max_hour: int,
                              tomorrow_temp_max: float,
                              ) -> LinearRegression:
    KEY_INTERVAL1_HOUR = 'I1H'
    KEY_INTERVAL1_TEMP = 'I1T'
    KEY_INTERVAL2_HOUR = 'I2H'
    KEY_INTERVAL2_TEMP = 'I2T'

    def get_intervals(temp_min_: float, temp_max_: float, hour_temp_min_: int, hour_temp_max_: int) -> dict:
        result = {}
        if hour_temp_min_ < hour_temp_max_:
            result[KEY_INTERVAL1_HOUR] = hour_temp_min_
            result[KEY_INTERVAL1_TEMP] = temp_min_
            result[KEY_INTERVAL2_HOUR] = hour_temp_max_
            result[KEY_INTERVAL2_TEMP] = temp_max_
        else:
            result[KEY_INTERVAL2_HOUR] = hour_temp_min_
            result[KEY_INTERVAL2_TEMP] = temp_min_
            result[KEY_INTERVAL1_HOUR] = hour_temp_max_
            result[KEY_INTERVAL1_TEMP] = temp_max_

        return result

    dict_yesterday_interval_points = get_intervals(yesterday_temp_min, yesterday_temp_max, yesterday_temp_min_hour,
                                                   yesterday_temp_max_hour)
    dict_today_interval_points = get_intervals(temp_min, temp_max, hour_temp_min, hour_temp_max)
    dict_tomorrow_interval_points = get_intervals(tomorrow_temp_min, tomorrow_temp_max, tomorrow_temp_min_hour,
                                                  tomorrow_temp_max_hour)

    def get_temperature_with_interval_points(yesterday_point2_hour: int, yesterday_point2_temp: float,
                                             today_point1_hour: int, today_point1_temp: float, today_point2_hour: int,
                                             today_point2_temp: float,
                                             tomorrow_point1_hour: int, tomorrow_point1_temp: float,
                                             ) -> LinearRegression:

        if hour_to_predict < today_point1_hour:
            # Linear with yesterday_point2 and today_point1
            result_temp = get_temperature_model(yesterday_point2_temp, today_point1_temp, yesterday_point2_hour,
                                                today_point1_hour)
        elif hour_to_predict < today_point2_hour:
            # Linear with today_point1 and today_point2
            result_temp = get_temperature_model(today_point1_temp, today_point2_temp, today_point1_hour,
                                                today_point2_hour)
        else:
            # Linear with today_point2 and tomorrow_point1
            result_temp = get_temperature_model(today_point2_temp, tomorrow_point1_temp, today_point2_hour,
                                                tomorrow_point1_hour)
        return result_temp

    return get_temperature_with_interval_points(
        dict_yesterday_interval_points[KEY_INTERVAL2_HOUR], dict_yesterday_interval_points[KEY_INTERVAL2_TEMP],
        dict_today_interval_points[KEY_INTERVAL1_HOUR], dict_today_interval_points[KEY_INTERVAL1_TEMP],
        dict_today_interval_points[KEY_INTERVAL2_HOUR], dict_today_interval_points[KEY_INTERVAL2_TEMP],
        dict_tomorrow_interval_points[KEY_INTERVAL1_HOUR], dict_tomorrow_interval_points[KEY_INTERVAL1_TEMP]
    )