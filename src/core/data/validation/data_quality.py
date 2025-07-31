import pandas as pd


def check_missing_timestamps(df: pd.DataFrame, expected_freq="1min"):
    df = df.sort_index()
    missing = df.index.to_series().asfreq(expected_freq).isna().sum()
    return {"missing_timestamps": int(missing)}


def check_price_bounds(df: pd.DataFrame):
    issues = df[
        (df["open"] <= 0) | (df["high"] <= 0) | (df["low"] <= 0) | (df["close"] <= 0)
    ]
    return {"out_of_range_prices": len(issues)}


def check_duplicate_entries(df: pd.DataFrame):
    return {"duplicates": df.duplicated().sum()}


def check_volume_anomalies(df: pd.DataFrame):
    return {"zero_volume": (df["volume"] <= 0).sum()}
