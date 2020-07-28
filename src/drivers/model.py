import argparse
from argparse import Namespace

from general.operations.dataframe_operations import load_dataframe_from_csv

from bicimad.constants.paths import *
from src.bicimad.constants.weather_constants import *
from src.bicimad.constants.bikes_constants import *

from bicimad.modeling.utils import prepare_data
from bicimad.modeling.linear_regression import *

# Before executing: export PYTHONPATH="/home/irene/dev/keepler-prueba/keepler-bicimad:$PYTHONPATH"

def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    dataset = load_dataframe_from_csv(create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency)))
    print(dataset.shape)


def main():
    # args: --home-path /home/irene/dev/keepler-prueba/keepler-bicimad --sampling-frequency daily --model-type linear-regression
    print("[data-modeling] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Cleaning')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')
    parser.add_argument('--sampling-frequency', type=str, default='daily', metavar='S',
                        help='Sampling frequency of data: daily/hourly ')
    parser.add_argument('--model-type', type=str, default='linear-regression', metavar='M',
                        help = 'Type of model to create prediction forecasting model {linear-regression, ...}')

    args: Namespace = parser.parse_args()
    print("[data-modeling] Setting home path as: {}".format(args.home_path))
    print("[data-modeling] Creating [{}] model for {} forecasting".format(args.model_type, args.sampling_frequency))
    runner(args)
    #print("[data-modeling] Success: Prepared data stored in {}.".format(create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency))))


if __name__ == '__main__':
    main()