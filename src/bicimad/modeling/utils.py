import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

from bicimad.constants.model import CATEGORICAL_COLUMNS_DAILY, TEST_SIZE, COLUMNS_TO_TRANSFORM_TYPE_DAILY
from bicimad.modeling.linear_regression import create_linear_regression_model
from bicimad.operations.cleaning import transform_types_dataset
from pandas import DataFrame as DataFrame


def split_data(df: DataFrame, test_size=0.2):
    # TODO better transform to numpy?
    return train_test_split(df, test_size=test_size)


def encode_categorical(df: DataFrame, categorical_columns: list) -> DataFrame:
    return pd.get_dummies(df, columns=categorical_columns)


def prepare_data(df: DataFrame):
    df_types_transformed = transform_types_dataset(df, COLUMNS_TO_TRANSFORM_TYPE_DAILY)
    df_encoded = encode_categorical(df_types_transformed, CATEGORICAL_COLUMNS_DAILY)
    return split_data(df_encoded, TEST_SIZE)


def train(model, df_train, features_columns, target_column):
    return model.fit(df_train[features_columns], df_train[target_column])


def predict(model, test_features):
    return model.predict(test_features)


def evaluate(predictions, test_target):

    # TODO implement parametrization of metrics selection

    def mean_absolute_percentage_error(target_true, target_predicted):
        return np.mean(np.abs((target_true - target_predicted) / target_true)) * 100

    metrics_result = {}
    metrics_result['mae'] = mean_absolute_error(test_target, predictions)
    metrics_result['mse']  = mean_squared_error(test_target, predictions)
    metrics_result['r2'] = r2_score(test_target, predictions)
    metrics_result['mape'] = mean_absolute_percentage_error(test_target, predictions)
    metrics_result['acc'] = 100 - metrics_result['mape']
    return metrics_result


def grid_search_cv(estimator, parameters_grid, train_features, train_target):
    grid_search = GridSearchCV(estimator=estimator, param_grid=parameters_grid)
    grid_search = grid_search.fit(train_features, train_target)
    return grid_search

