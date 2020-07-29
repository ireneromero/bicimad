import argparse
from argparse import Namespace

from bicimad.constants.paths import PATH_BIKES_RAW, PATH_BIKES_CLEAN
from bicimad.operations.cleaning import clean_bikes_data
from general.operations.dataframe_operations import load_dataframe_from_csv, save_dataframe


# Before executing: export PYTHONPATH="/home/irene/dev/keepler-prueba/keepler-bicimad:$PYTHONPATH"

def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    df_bikes = load_dataframe_from_csv(create_path(args.home_path, PATH_BIKES_RAW))
    df_bikes = clean_bikes_data(df_bikes, without_employees=True, remove_outliers=True)
    save_dataframe(df_bikes, create_path(args.home_path, PATH_BIKES_CLEAN))


def main():
    # args: --home-path /home/irene/dev/keepler-prueba/keepler-bicimad
    print("[data-cleaning] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Cleaning')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')

    args: Namespace = parser.parse_args()
    print("[data-cleaning] Setting home path as: {}".format(args.home_path))

    runner(args)
    print("[data-cleaning] Success: Clean data stored in {}.".format(create_path(args.home_path, PATH_BIKES_CLEAN)))


if __name__ == '__main__':
    main()