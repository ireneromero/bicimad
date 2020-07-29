import pandas as pd
from bicimad.constants.rides import COL_BIKES_ID_PLUG_BASE, COL_BIKES_ID_UNPLUG_BASE, \
    COL_BIKES_ID_PLUG_STATION, COL_BIKES_ID_UNPLUG_STATION, COL_BIKES_USER_TYPE, COL_BIKES_AGE_RANGE, \
    COL_BIKES_UNPLUG_TIMESTAMP, COL_BIKES_DAY_OF_WEEK, COL_BIKES_HOUR, COL_BIKES_MONTH, COL_BIKES_DAY, COL_BIKES_DATE, \
    COL_BIKES_TRAVEL_TIME, USER_TYPE_EMPLOYEE
from bicimad.constants.cleaning.mappers import STATIONS_DICT, DAY_OF_WEEK_DICT
from bicimad.constants.weather import COL_WEATHER_TEMP_MEAN, COL_WEATHER_RAIN, COL_WEATHER_WIND_MEAN, \
    COL_WEATHER_TEMP_MIN, COL_WEATHER_TEMP_MAX
from pandas import DataFrame as DataFrame


UPPER_QUANTILE = 0.95
LOWER_QUANTILE = 0.05


def clean_bikes_data(df: DataFrame, without_employees: bool = False, remove_outliers: bool = False) -> DataFrame:
    # TODO modify without_employees to with_employees to better usability
    # TODO refactor -> move remove outliers and remove employee data to prepare_dataset.py
    df = transform_types_bikes(df)
    df = clean_stations(df)
    df = clean_date_bikes(df)
    if remove_outliers:
        df = remove_outliers_travel_time(df)
    if without_employees:
        df = filter_out_employees(df)
    return df


def transform_types_bikes(df: DataFrame) -> DataFrame:
    df[COL_BIKES_ID_PLUG_BASE] = df[COL_BIKES_ID_PLUG_BASE].apply(str)
    df[COL_BIKES_ID_UNPLUG_BASE] = df[COL_BIKES_ID_UNPLUG_BASE].apply(str)
    df[COL_BIKES_ID_PLUG_STATION] = df[COL_BIKES_ID_PLUG_STATION].apply(str)
    df[COL_BIKES_ID_UNPLUG_STATION] = df[COL_BIKES_ID_UNPLUG_STATION].apply(str)
    df[COL_BIKES_USER_TYPE] = df[COL_BIKES_USER_TYPE].apply(str)
    df[COL_BIKES_AGE_RANGE] = df[COL_BIKES_AGE_RANGE].apply(str)
    df[COL_BIKES_UNPLUG_TIMESTAMP] = pd.to_datetime(df[COL_BIKES_UNPLUG_TIMESTAMP])
    return df


def clean_station(station: str) -> str:
    return STATIONS_DICT.get(station, station)


def clean_stations(df: DataFrame) -> DataFrame:
    df[COL_BIKES_ID_PLUG_BASE] = df[COL_BIKES_ID_PLUG_BASE].map(
         clean_station)
    df[COL_BIKES_ID_UNPLUG_BASE] = df[COL_BIKES_ID_UNPLUG_BASE].map(
         clean_station)
    return df


def clean_date_bikes(df: DataFrame) -> DataFrame:
    df[COL_BIKES_DAY_OF_WEEK] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.dayofweek\
        .map(DAY_OF_WEEK_DICT)
    df[COL_BIKES_HOUR] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.hour
    df[COL_BIKES_MONTH] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.month
    df[COL_BIKES_DAY] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.day
    df[COL_BIKES_DATE] = df[COL_BIKES_UNPLUG_TIMESTAMP].dt.date
    return df


def remove_outliers_travel_time(df: DataFrame) -> DataFrame:
    upper_limit = df[COL_BIKES_TRAVEL_TIME].quantile(UPPER_QUANTILE)
    lower_limit = df[COL_BIKES_TRAVEL_TIME].quantile(LOWER_QUANTILE)
    return df[(df[COL_BIKES_TRAVEL_TIME] < upper_limit) & (df[COL_BIKES_TRAVEL_TIME] > lower_limit)]


def filter_out_employees(df: DataFrame) -> DataFrame:
    # remove rows where user_type = 3 (bicimad employee)
    return df[df[COL_BIKES_USER_TYPE] != USER_TYPE_EMPLOYEE]


def clean_weather_data(df: DataFrame) -> DataFrame:
    return transform_types_weather(df)


def column_to_float_format(df: DataFrame, column_name: str) -> DataFrame:
    df[column_name] = df[column_name].astype(str).str.replace(',', '.')
    return df


def column_to_numeric(df: DataFrame, column_name: str) -> DataFrame:
    df[column_name] = pd.to_numeric(df[column_name], downcast='float')
    return df


# TODO refactor these funcions (transform_types_*) to a single one?
def transform_types_weather(df: DataFrame) -> DataFrame:
    columns_to_transform = [COL_WEATHER_TEMP_MEAN, COL_WEATHER_RAIN, COL_WEATHER_WIND_MEAN]
    for column in columns_to_transform:
        df = column_to_float_format(df, column)
        df = column_to_numeric(df, column)
    return df


def transform_types_dataset(df:DataFrame, columns_to_transform) -> DataFrame:
    for column in columns_to_transform:
        df = column_to_float_format(df, column)
        df = column_to_numeric(df, column)
    return df




