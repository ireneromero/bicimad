import argparse
from argparse import Namespace
import json

from bicimad.constants.model_constants import FEATURES_DAILY, TARGET
from bicimad.constants.paths import PATH_DATASET, PATH_MODEL_DEEPLEARNING_MODEL, PATH_MODEL_DEEPLEARNING_METRICS
from bicimad.modeling.deep_learning import deep_learning_model, save_model
from bicimad.modeling.linear_regression import create_linear_regression_model
from bicimad.modeling.utils import prepare_data
from general.operations.dataframe_operations import load_dataframe_from_csv


# Before executing: export PYTHONPATH="/home/irene/dev/keepler-prueba/keepler-bicimad:$PYTHONPATH"

def create_path(home_path: str, relative_path: str) -> str:
    return home_path + '/' + relative_path


def runner(args: Namespace) -> None:
    dataset = load_dataframe_from_csv(create_path(args.home_path, PATH_DATASET.get(args.sampling_frequency)))

    if args.model_type == 'linear_regression':
        dataset_train, dataset_test = prepare_data(dataset)
        model = create_linear_regression_model()

    elif args.model_type == 'deep-learning':
        # TODO only works for (deep learning, daily)
        net, metrics = deep_learning_model(dataset)
        metrics = {metric_name: str(metric_value) for metric_name, metric_value in metrics.items()}
        save_model(net, create_path(args.home_path, PATH_MODEL_DEEPLEARNING_MODEL))
        with open(create_path(args.home_path, PATH_MODEL_DEEPLEARNING_METRICS), 'w') as metrics_file: # TODO remove with?
            metrics_file.write(json.dumps(metrics))


def main():
    # args: --home-path /home/irene/dev/keepler-prueba/keepler-bicimad --sampling-frequency daily --model-type deep-learning
    print("[data-modeling] Starting ... ")
    parser = argparse.ArgumentParser(description='[BiciMad Project] Data Forecasting Model')
    parser.add_argument('--home-path', type=str, default='.', metavar='H',
                        help='home path')
    parser.add_argument('--sampling-frequency', type=str, default='daily', metavar='S',
                        help='Sampling frequency of data: daily/hourly ')
    parser.add_argument('--model-type', type=str, default='deep-learning', metavar='M',
                        help = 'Type of model to create prediction forecasting model {linear-regression, deep-learning}')

    args: Namespace = parser.parse_args()
    print("[data-modeling] Setting home path as: {}".format(args.home_path))
    print("[data-modeling] Creating [{}] model for {} forecasting".format(args.model_type, args.sampling_frequency))
    runner(args)
    print("[data-modeling] Success: Deep learning model state dictionary stored in {}.".format(create_path(args.home_path, PATH_MODEL_DEEPLEARNING_MODEL)))


if __name__ == '__main__':
    main()