import pandas as pd
from bicimad.constants.model_constants import CATEGORICAL_COLUMNS_DAILY, TEST_SIZE
from pandas import DataFrame as DataFrame
import math
from sklearn.model_selection import train_test_split
from sklearn import metrics


def split_data(df: DataFrame, test_size=0.2):
    # TODO better transform to numpy?
    return train_test_split(df, test_size)

def encode_categorical(df: DataFrame, categorical_columns: list) -> DataFrame:
    return pd.get_dummies(df, columns=categorical_columns)

def prepare_data(df: DataFrame):
    df_encoded = encode_categorical(df, CATEGORICAL_COLUMNS_DAILY)
    print(df_encoded.head())
    df_train, df_test = split_data(df_encoded, TEST_SIZE)
    return (df_train, df_test)


def evaluate(model, test_features, test_target, metric='rmse') -> int:
    predictions = model.predict(test_features)
    if metric == 'rmse':
        rmse = math.sqrt(metrics.mean_absolute_error(predictions, test_target))
    return rmse