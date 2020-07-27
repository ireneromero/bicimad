import argparse
from argparse import Namespace
from src.general.operations.dataframe_operations import load_dataframe_from_csv, load_dataframe_from_json, save_dataframe
from src.bicimad.operations.cleaning_operations import clean_weather_data
from src.bicimad.operations.aggregation_operations import prepare_daily_data

from src.bicimad.constants.paths import *
from src.bicimad.constants.weather_constants import *
from src.bicimad.constants.bikes_constants import *

# Before executing: export PYTHONPATH="/home/irene/dev/keepler-prueba/keepler-bicimad:$PYTHONPATH"

def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    df_bikes_clean = load_dataframe_from_csv(create_path(args.home_path, path_bikes_clean), parse_dates=[COL_BIKES_DATE])
    df_weather = load_dataframe_from_json(create_path(args.home_path, path_aemet_per_day), parse_dates=[COL_WEATHER_DATE])
    df_weather = clean_weather_data(df_weather)
    if args.sampling_frequency == 'daily': # extract daily/hourly value as constant
        df_prepared = prepare_daily_data(df_bikes_clean, df_weather)
    elif args.sampling_frequency == 'hourly':
        # TODO
        pass
    # TODO implement else, return error
    save_dataframe(df_prepared, create_path(args.home_path, path_dataset.get(args.sampling_frequency)))


def main():
    # args: --home-path /home/irene/dev/keepler-prueba/keepler-bicimad --sampling-frequency daily
    print("[data-preparation] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Cleaning')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')
    parser.add_argument('--sampling-frequency', type=str, default='daily', metavar='S',
                        help='Sampling frequency of data: daily/hourly ')

    args: Namespace = parser.parse_args()
    print("[data-preparation] Setting home path as: {}".format(args.home_path))
    print("[data-preparation] Preparing [{}] data".format(args.sampling_frequency))
    runner(args)
    print("[data-preparation] Success: Prepared data stored in {}.".format(create_path(args.home_path, path_dataset.get(args.sampling_frequency))))


if __name__ == '__main__':
    main()