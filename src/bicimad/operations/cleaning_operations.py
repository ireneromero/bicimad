import pandas as pd
import src.bicimad.constants.cleaning.mappers
from src.bicimad.constants.bikes_constants import *
from src.bicimad.constants.weather_constants import *

UPPER_QUANTILE = 0.95
LOWER_QUANTILE = 0.05


def clean_bikes_data(df: pd.DataFrame, without_employees: bool = False, remove_outliers: bool = False) -> pd.DataFrame:
    df = transform_types_bikes(df)
    df = clean_stations(df)
    df = clean_date_bikes(df)
    if remove_outliers:
        df = remove_outliers_travel_time(df)
    if without_employees:
        df = filter_out_employees(df)
    return df


def transform_types_bikes(df: pd.DataFrame) -> pd.DataFrame:
    df[COL_BIKES_ID_PLUG_BASE] = df[COL_BIKES_ID_PLUG_BASE].apply(str)
    df[COL_BIKES_ID_UNPLUG_BASE] = df[COL_BIKES_ID_UNPLUG_BASE].apply(str)
    df[COL_BIKES_ID_PLUG_STATION] = df[COL_BIKES_ID_PLUG_STATION].apply(str)
    df[COL_BIKES_ID_UNPLUG_STATION] = df[COL_BIKES_ID_UNPLUG_STATION].apply(str)
    df[COL_BIKES_USER_TYPE] = df[COL_BIKES_USER_TYPE].apply(str)
    df[COL_BIKES_AGE_RANGE] = df[COL_BIKES_AGE_RANGE].apply(str)
    df[COL_BIKES_UNPLUG_TIMESTAMP] = pd.to_datetime(df[COL_BIKES_UNPLUG_TIMESTAMP])
    return df


def clean_station(station: str) -> str:
    return src.bicimad.constants.cleaning.mappers.stations_dict.get(station, station)


def clean_stations(df: pd.DataFrame) -> pd.DataFrame:
    df[COL_BIKES_ID_PLUG_BASE] = df[COL_BIKES_ID_PLUG_BASE].map(
         clean_station)
    df[COL_BIKES_ID_UNPLUG_BASE] = df[COL_BIKES_ID_UNPLUG_BASE].map(
         clean_station)
    return df


def clean_date_bikes(df: pd.DataFrame) -> pd.DataFrame:
    df[COL_BIKES_DAY_OF_WEEK] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.dayofweek\
        .map(src.bicimad.constants.cleaning.mappers.day_of_week_dict)
    df[COL_BIKES_HOUR] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.hour
    df[COL_BIKES_MONTH] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.month
    df[COL_BIKES_DAY] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.day
    df[COL_BIKES_DATE] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.date
    return df


def remove_outliers_travel_time(df: pd.DataFrame) -> pd.DataFrame:
    upper_limit = df[COL_BIKES_TRAVEL_TIME].quantile(UPPER_QUANTILE)
    lower_limit = df[COL_BIKES_TRAVEL_TIME].quantile(LOWER_QUANTILE)
    return df[(df[COL_BIKES_TRAVEL_TIME] < upper_limit) & (df[COL_BIKES_TRAVEL_TIME] > lower_limit)]


def filter_out_employees(df: pd.DataFrame) -> pd.DataFrame:
    # remove rows where user_type = 3 (bicimad employee)
    return df[df[COL_BIKES_USER_TYPE != USER_TYPE_EMPLOYEE]]


def transform_col_to_date(col: pd.Series) -> pd.Series:
    return pd.to_datetime(col)


def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    return transform_types_weather(df)


def transform_types_weather(df: pd.DataFrame) -> pd.DataFrame:
    # TODO think about refactoring this?
    df[COL_WEATHER_TEMP_MEAN] = df[COL_WEATHER_TEMP_MEAN].str.replace(',', '.')
    df[COL_WEATHER_RAIN] = df[COL_WEATHER_RAIN].str.replace(',', '.')
    df[COL_WEATHER_WIND_MEAN] = df[COL_WEATHER_WIND_MEAN].str.replace(',', '.')

    df[COL_WEATHER_TEMP_MEAN] = pd.to_numeric(df[COL_WEATHER_TEMP_MEAN], downcast='float')
    df[COL_WEATHER_RAIN] = pd.to_numeric(df[COL_WEATHER_RAIN], downcast='float')
    df[COL_WEATHER_WIND_MEAN] = pd.to_numeric(df[COL_WEATHER_WIND_MEAN], downcast='float')

    return df




