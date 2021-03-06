import argparse
from argparse import Namespace
import json

from bicimad.constants.paths import PATH_DATASET, PATH_RESULTS
from bicimad.modeling.deep_learning import deep_learning_model, save_model
from general.operations.dataframe_operations import load_dataframe_from_csv


def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    dataset = load_dataframe_from_csv(create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency)))

    net, metrics = deep_learning_model(dataset)
    metrics = {metric_name: str(metric_value) for metric_name, metric_value in metrics.items()}
    save_model(net, create_path(args.home_path, PATH_RESULTS[args.sampling_frequency]['deep-learning']['model']))
    with open(create_path(args.home_path, PATH_RESULTS[args.sampling_frequency]['deep-learning']['metrics']), 'w') as metrics_file: # TODO refactor this as a function
        metrics_file.write(json.dumps(metrics))


def main():
    print("[data-modeling][deep-learning] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Forecasting Model')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')
    parser.add_argument('--sampling-frequency', type=str, default='daily', metavar='S',
                        help='Sampling frequency of data: only daily supported ')

    args: Namespace = parser.parse_args()

    if (args.sampling_frequency == 'hourly'):
        print("[data-modeling][deep-learning] Only daily mode supported.")
        exit()

    print("[data-modeling][deep-learning] Setting home path as: {}".format(args.home_path))
    print("[data-modeling][deep-learning] Creating model for {} forecasting".format(args.sampling_frequency))
    runner(args)
    print("[data-modeling][deep-learning] Success: deep learning model state dictionary stored in {}.".format(create_path(args.home_path,
                                                                                PATH_RESULTS[args.sampling_frequency]['deep-learning']['model'])))
    print("[data-modeling][deep-learning] Success: metrics stored in {}.".format(create_path(args.home_path,
                                                                                    PATH_RESULTS[args.sampling_frequency]['deep-learning']['metrics'])))


if __name__ == '__main__':
    main()
