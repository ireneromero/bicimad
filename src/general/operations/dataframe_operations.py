import pandas as pd


def load_dataframe_from_csv(path: str, encoding: str = 'utf-8', sep: str = ',', parse_dates: list = []) -> pd.DataFrame:
    return pd.read_csv(path, encoding, sep, parse_dates=parse_dates)


def load_dataframe_from_json(path: str, parse_dates: list = []) -> pd.DataFrame:
    return pd.read_json(path, orient='records', convert_dates=parse_dates)


def save_dataframe(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)

