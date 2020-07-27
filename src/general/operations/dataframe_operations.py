import pandas as pd

def load_dataframe(path: str, encoding: str = 'utf-8', sep: str = ',') -> pd.DataFrame:
    return pd.read_csv(path, encoding, sep)


def save_dataframe(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)

