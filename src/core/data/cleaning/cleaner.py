# src/core/data/cleaning/cleaner.py
import pandas as pd


class DataCleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        # Standardize symbol column (if exists)
        if "symbol" in df.columns:
            df["symbol"] = df["symbol"].str.upper()

        # Set index to datetime if not already
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        # Ensure timezone-awareness (UTC)
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")
        else:
            df.index = df.index.tz_convert("UTC")

        return df
