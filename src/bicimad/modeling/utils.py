import pandas as pd
from bicimad.constants.model_constants import CATEGORICAL_COLUMNS_DAILY, TEST_SIZE, COLUMNS_TO_TRANSFORM_TYPE_DAILY
from bicimad.modeling.linear_regression import create_linear_regression_model
from bicimad.operations.cleaning_operations import transform_types_dataset
from pandas import DataFrame as DataFrame
import math
from sklearn.model_selection import train_test_split
from sklearn import metrics


def split_data(df: DataFrame, test_size=0.2):
    # TODO better transform to numpy?
    return train_test_split(df, test_size=test_size)

def encode_categorical(df: DataFrame, categorical_columns: list) -> DataFrame:
    return pd.get_dummies(df, columns=categorical_columns)

def prepare_data(df: DataFrame):

    df_types_transformed = transform_types_dataset(df, COLUMNS_TO_TRANSFORM_TYPE_DAILY)
    df_encoded = encode_categorical(df_types_transformed, CATEGORICAL_COLUMNS_DAILY)
    return split_data(df_encoded, TEST_SIZE)

def create_model(model_type: str):
    if model_type == 'linear-regression':
        return create_linear_regression_model()
    else:
        return create_linear_regression_model()


def train(model, df_train, features_columns, target_column):
    return model.fit(df_train[features_columns], df_train[target_column])


def evaluate(model, df_test, features_columns, target_column, metrics: list = ['rmse']) -> int:
    metrics_result = {}
    #TODO implement for other metrics
    predictions = model.predict(df_test[features_columns])
    if 'rmse' in metrics:
        metrics_result['rmse'] = math.sqrt(metrics.mean_absolute_error(predictions, df_test[target_column]))
    if 'mae' in metrics:
        # TODO
        pass
    return metrics_result