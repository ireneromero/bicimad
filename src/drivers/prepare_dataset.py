import argparse
from argparse import Namespace

from bicimad.constants.paths import PATH_BIKES_CLEAN, PATH_AEMET_PER_DAY, PATH_DATASET
from bicimad.constants.rides import COL_BIKES_DATE
from bicimad.constants.weather import COL_WEATHER_DATE
from general.operations.dataframe_operations import load_dataframe_from_csv, load_dataframe_from_json, save_dataframe
from bicimad.operations.cleaning import clean_weather_data
from bicimad.operations.aggregation import prepare_daily_data, prepare_hourly_data


def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    df_bikes_clean = load_dataframe_from_csv(create_path(args.home_path, PATH_BIKES_CLEAN), parse_dates=[COL_BIKES_DATE])
    df_weather = load_dataframe_from_json(create_path(args.home_path, PATH_AEMET_PER_DAY), parse_dates=[COL_WEATHER_DATE])
    df_weather = clean_weather_data(df_weather)
    if args.sampling_frequency == 'daily': # extract daily/hourly value as constant
        df_prepared = prepare_daily_data(df_bikes_clean, df_weather)
    elif args.sampling_frequency == 'hourly':
        df_prepared = prepare_hourly_data(df_bikes_clean, df_weather)
        pass
    # TODO implement else, return error
    save_dataframe(df_prepared, create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency)))


def main():
    print("[data-preparation] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Cleaning')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')
    parser.add_argument('--sampling-frequency', type=str, default='hourly', metavar='S',
                        help='Sampling frequency of data: daily/hourly ')

    args: Namespace = parser.parse_args()
    print("[data-preparation] Setting home path as: {}".format(args.home_path))
    print("[data-preparation] Preparing [{}] data".format(args.sampling_frequency))
    runner(args)
    print("[data-preparation] Success: Prepared data stored in {}.".format(create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency))))


if __name__ == '__main__':
    main()