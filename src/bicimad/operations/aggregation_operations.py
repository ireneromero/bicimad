import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from src.general.operations.dataframe_operations import load_dataframe_from_csv, save_dataframe
from bicimad.constants.bikes_constants import *
from bicimad.constants.weather_constants import *


def preprocess_rides_per_day(df: pd.DataFrame) -> pd.DataFrame:
    # this dataframe should have a date column (parsed as datetime)
    return df.groupby([COL_BIKES_DATE, COL_BIKES_DAY_OF_WEEK]).size().reset_index(name=COL_BIKES_RIDES)


def preprocess_rides_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby([COL_BIKES_DATE, COL_BIKES_DAY_OF_WEEK, COL_BIKES_HOUR]).size().reset_index(name=COL_BIKES_RIDES)

def add_mean_rides_for_day(df: pd.DataFrame) -> pd.DataFrame:
    mean_for_weekday = df.groupby(COL_BIKES_DAY_OF_WEEK)[COL_BIKES_RIDES].mean().to_dict()
    df[COL_BIKES_RIDES_MEAN_WEEKDAY] = df[COL_BIKES_DAY_OF_WEEK].map(mean_for_weekday)
    return df

def add_mean_rides_for_day_and_hour(df: pd.DataFrame) -> pd.DataFrame:
    mean_for_weekday_and_hour = df.groupby([COL_BIKES_DAY_OF_WEEK, COL_BIKES_HOUR])[COL_BIKES_RIDES].mean().to_dict()

    def add_mean_rides_for_day_and_hour_for_row(row):
        return mean_for_weekday_and_hour.get((row[COL_BIKES_DAY_OF_WEEK], row[COL_BIKES_HOUR]))

    df[COL_BIKES_RIDES_MEAN_WEEKDAY_HOUR] = df.apply(lambda row: add_mean_rides_for_day_and_hour_for_row(row), axis=1)
    return df


def add_weather_data_per_day(df: pd.DataFrame, df_weather: pd.DataFrame) -> pd.DataFrame:
    return df.merge(df_weather[[COL_WEATHER_DATE, COL_WEATHER_TEMP_MEAN, COL_WEATHER_RAIN, COL_WEATHER_WIND_MEAN,
                                COL_WEATHER_HOUR_TEMP_MAX, COL_WEATHER_HOUR_TEMP_MIN, COL_WEATHER_TEMP_MAX, COL_WEATHER_TEMP_MIN]],
             how='left',
             left_on=COL_BIKES_DATE,
             right_on=COL_WEATHER_DATE)


def prepare_daily_data(df: pd.DataFrame, df_weather: pd.DataFrame) -> pd.DataFrame:
    df_rides_per_day = preprocess_rides_per_day(df)
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


def get_hourly_weather(df: pd.DataFrame) -> pd.DataFrame:
    df[COL_WEATHER_RAIN_HOURLY] = df[COL_WEATHER_RAIN]
    df[COL_WEATHER_WIND_HOURLY] = df[COL_WEATHER_WIND_MEAN]
    #print(df[COL_WEATHER_HOUR_TEMP_MIN].isna().sum())
    df[COL_WEATHER_HOUR_TEMP_MIN] = df[COL_WEATHER_HOUR_TEMP_MIN].astype(str).str[:2].astype(int)
    df[COL_WEATHER_HOUR_TEMP_MAX] = df[COL_WEATHER_HOUR_TEMP_MAX].astype(str).str[:2].astype(int)
    df[COL_WEATHER_TEMP_HOURLY] = df.apply(lambda row: get_temperature_simple_per_row(row), axis=1)
    return df



def prepare_hourly_data(df: pd.DataFrame, df_weather: pd.DataFrame) -> pd.DataFrame:
    df_rides_per_hour = preprocess_rides_per_hour(df)
    df_rides_per_hour = add_mean_rides_for_day_and_hour(df_rides_per_hour)
    df_hourly = add_weather_data_per_day(df_rides_per_hour, df_weather)
    return get_hourly_weather(df_hourly).drop([COL_WEATHER_TEMP_MEAN,
                                               COL_WEATHER_RAIN,
                                               COL_WEATHER_WIND_MEAN,
                                               COL_WEATHER_HOUR_TEMP_MIN,
                                               COL_WEATHER_HOUR_TEMP_MAX], axis=1)