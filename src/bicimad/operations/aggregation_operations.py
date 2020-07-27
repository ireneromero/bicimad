import pandas as pd
from src.general.operations.dataframe_operations import load_dataframe_from_csv, save_dataframe
from src.bicimad.constants.bikes_constants import *
from src.bicimad.constants.weather_constants import *


def preprocess_rides_per_day(df: pd.DataFrame) -> pd.DataFrame:
    # this dataframe should have a date column (parsed as datetime)
    return df.groupby([COL_BIKES_DATE, COL_BIKES_DAY_OF_WEEK]).size().reset_index(name=COL_BIKES_RIDES)


def add_weather_data_per_day(df: pd.DataFrame, df_weather: pd.DataFrame) -> pd.DataFrame:
    return df.merge(df_weather[[COL_WEATHER_DATE, COL_WEATHER_TEMP_MEAN, COL_WEATHER_RAIN, COL_WEATHER_WIND_MEAN]],
             how='left',
             left_on=COL_BIKES_DATE,
             right_on=COL_WEATHER_DATE)


def prepare_daily_data(df: pd.DataFrame, df_weather: pd.DataFrame) -> pd.DataFrame:
    df_rides_per_day = preprocess_rides_per_day(df)
    df_daily = add_weather_data_per_day(df_rides_per_day, df_weather)
    return df_daily

