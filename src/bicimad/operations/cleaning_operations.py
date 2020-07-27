import pandas as pd
import src.bicimad.constants.cleaning.mappers
from src.bicimad.constants.bikes_constants import *

UPPER_QUANTILE = 0.95
LOWER_QUANTILE = 0.05


def clean(df: pd.DataFrame, without_employees: bool = False, remove_outliers: bool = False) -> pd.DataFrame:
    df = transform_types(df)
    df = clean_stations(df)
    df = clean_date(df)
    if remove_outliers:
        df = remove_outliers_travel_time(df)
    if without_employees:
        df = filter_out_employees(df)
    return df


def transform_types(df: pd.DataFrame) -> pd.DataFrame:
    df[bikes_col_id_plug_base] = df[bikes_col_id_plug_base].apply(str)
    df[bikes_col_id_unplug_base] = df[bikes_col_id_unplug_base].apply(str)
    df[bikes_col_id_plug_station] = df[bikes_col_id_plug_station].apply(str)
    df[bikes_col_id_unplug_station] = df[bikes_col_id_unplug_station].apply(str)
    df[bikes_col_user_type] = df[bikes_col_user_type].apply(str)
    df[bikes_col_age_range] = df[bikes_col_age_range].apply(str)
    df[bikes_col_unplug_timestamp] = pd.to_datetime(df[bikes_col_unplug_timestamp])
    return df


def clean_station(station: str) -> str:
    return src.bicimad.constants.cleaning.mappers.stations_dict.get(station, station)


def clean_stations(df: pd.DataFrame) -> pd.DataFrame:
    df[bikes_col_id_plug_base] = df[bikes_col_id_plug_base].map(
         clean_station)
    df[bikes_col_id_unplug_base] = df[bikes_col_id_unplug_base].map(
         clean_station)
    return df


def clean_date(df: pd.DataFrame) -> pd.DataFrame:
    df[bikes_col_day_of_week] = df[bikes_col_unplug_timestamp].dt.dayofweek\
        .map(src.bicimad.constants.cleaning.mappers.day_of_week_dict)
    df[bikes_col_hour] = df[bikes_col_unplug_timestamp].dt.hour
    df[bikes_col_month] = df[bikes_col_unplug_timestamp].dt.month
    df[bikes_col_day] = df[bikes_col_unplug_timestamp].dt.day
    return df


def remove_outliers_travel_time(df: pd.DataFrame) -> pd.DataFrame:
    upper_limit = df[bikes_col_travel_time].quantile(UPPER_QUANTILE)
    lower_limit = df[bikes_col_travel_time].quantile(LOWER_QUANTILE)
    return df[(df[bikes_col_travel_time] < upper_limit) & (df[bikes_col_travel_time] > lower_limit)]

def filter_out_employees(df: pd.DataFrame) -> pd.DataFrame:
    # remove rows where user_type = 3 (bicimad employee)
    return df[df[bikes_col_user_type != user_type_employee]]




