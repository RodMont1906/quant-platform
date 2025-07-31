# src/core/data/providers/yahoo.py

from typing import Dict

import pandas as pd
import yfinance as yf

from core.data.providers.base import MarketDataProvider


class YahooFinanceAdapter(MarketDataProvider):
    """
    Adapter for Yahoo Finance using the yfinance library.
    Suitable for historical data only. No API key required.
    """

    async def get_historical_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        df = yf.download(
            tickers=symbol,
            start=start_date,
            end=end_date,
            interval=interval,
            progress=False,
            threads=False,
            auto_adjust=False,
        ).copy()

        if df.empty:
            raise ValueError(f"No data returned from Yahoo Finance for {symbol}")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns.name = None  # ✅ STRIP column level name like 'Price'

        df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            },
            inplace=True,
        )
        df.index.name = "timestamp"
        return df[["open", "high", "low", "close", "volume"]]

    async def get_real_time_quote(self, symbol: str) -> Dict:
        raise NotImplementedError("Yahoo Finance does not support real-time quotes")
