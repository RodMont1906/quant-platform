# src/core/data/cleaning/validator.py
import logging

import pandas as pd


class DataValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        # Ensure required columns exist
        required = {"open", "high", "low", "close", "volume"}
        if not required.issubset(df.columns):
            missing = required - set(df.columns)
            self.logger.warning(f"Missing columns: {missing}")
            raise ValueError(f"Missing required columns: {missing}")

        # Drop rows with NaNs
        nan_rows = df[df.isna().any(axis=1)]
        if not nan_rows.empty:
            self.logger.info(f"Dropping {len(nan_rows)} rows with NaNs")
        df = df.dropna()

        # Remove extreme price jumps (e.g. daily >50%)
        pct_change = df["close"].pct_change().abs()
        outliers = pct_change[pct_change > 0.5].index
        if not outliers.empty:
            self.logger.info(
                f"Removing {len(outliers)} outlier rows with price jump > 50%"
            )
            df = df.drop(outliers)

        # Remove zero-volume rows
        zero_vol = df[df["volume"] == 0]
        if not zero_vol.empty:
            self.logger.info(f"Removing {len(zero_vol)} zero-volume rows")
            df = df[df["volume"] != 0]

        # Enforce sorted index
        df = df.sort_index()

        return df
