import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(df: pd.DataFrame, test_size=0.3) -> (pd.DataFrame, pd.DataFrame):
    # TODO better transform to numpy?
    return train_test_split(df, test_size)

def encode_categorical():
    pass

def train():
    pass

def test():
    pass

def cross_validation():
    pass

# TODO refactor to metrics module?
def rmse():
    pass

def mae():
    pass