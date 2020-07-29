import argparse
from argparse import Namespace
import json

from bicimad.constants.paths import PATH_DATASET, PATH_RESULTS
from bicimad.modeling.xgboost import xgboost_model
from general.operations.dataframe_operations import load_dataframe_from_csv


def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    dataset = load_dataframe_from_csv(create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency)))
    xgb_model, metrics = xgboost_model(dataset)
    metrics = {metric_name: str(metric_value) for metric_name, metric_value in metrics.items()}
    # TODO implement saving XGB model in create_path(args.home_path, PATH_RESULTS[args.sampling_frequency]['xgboost']['model']))
    with open(create_path(args.home_path, PATH_RESULTS[args.sampling_frequency]['xgboost']['metrics']), 'w') as metrics_file: # TODO refactor this as a function
        metrics_file.write(json.dumps(metrics))

def main():
    print("[data-modeling][xgboost] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Forecasting Model')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')
    parser.add_argument('--sampling-frequency', type=str, default='daily', metavar='S',
                        help='Sampling frequency of data: daily/hourly ')

    args: Namespace = parser.parse_args()
    print("[data-modeling][xgboost] Setting home path as: {}".format(args.home_path))
    print("[data-modeling][xgboost] Creating model for {} forecasting".format(args.sampling_frequency))
    runner(args)
    print("[data-modeling][xgboost] Success: RF model stored in {}.".format(create_path(args.home_path,
                                                                                PATH_RESULTS[args.sampling_frequency]['xgboost']['model'])))
    print("[data-modeling][xgboost] Success: metrics stored in {}.".format(create_path(args.home_path,
                                                                                    PATH_RESULTS[args.sampling_frequency]['xgboost']['metrics'])))

if __name__ == '__main__':
    main()
