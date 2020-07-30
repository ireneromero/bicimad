import argparse
from argparse import Namespace
import json

from bicimad.constants.paths import PATH_DATASET, PATH_RESULTS
from bicimad.modeling.deep_learning import deep_learning_model, save_model
from bicimad.modeling.random_forest import random_forest_model
from general.operations.dataframe_operations import load_dataframe_from_csv


def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    dataset = load_dataframe_from_csv(create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency)))
    rf_model, metrics, ft_importance = random_forest_model(dataset, args.sampling_frequency)
    metrics = {metric_name: str(metric_value) for metric_name, metric_value in metrics.items()}
    # TODO implement saving RF model in create_path(args.home_path, PATH_RESULTS[args.sampling_frequency]['random-forest']['model']))
    with open(create_path(args.home_path, PATH_RESULTS[args.sampling_frequency]['random-forest']['metrics']), 'w') as metrics_file: # TODO refactor this as a function
        metrics_file.write(json.dumps(metrics))
        metrics_file.write(json.dumps(rf_model.get_params()))

def main():
    print("[data-modeling][random-forest] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Forecasting Model')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')
    parser.add_argument('--sampling-frequency', type=str, default='daily', metavar='S',
                        help='Sampling frequency of data: daily/hourly ')

    args: Namespace = parser.parse_args()
    print("[data-modeling][random-forest] Setting home path as: {}".format(args.home_path))
    print("[data-modeling][random-forest] Creating model for {} forecasting".format(args.sampling_frequency))
    runner(args)
    print("[data-modeling][random-forest] Success: RF model stored in {}.".format(create_path(args.home_path,
                                                                                PATH_RESULTS[args.sampling_frequency]['random-forest']['model'])))
    print("[data-modeling][random-forest] Success: metrics stored in {}.".format(create_path(args.home_path,
                                                                                    PATH_RESULTS[args.sampling_frequency]['random-forest']['metrics'])))

if __name__ == '__main__':
    main()
