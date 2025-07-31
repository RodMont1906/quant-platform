# src/core/data/providers/base.py

from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd


class MarketDataProvider(ABC):
    """
    Abstract base class for any market data provider adapter.
    """

    @abstractmethod
    async def get_historical_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Retrieve historical OHLCV data.

        Returns:
            pd.DataFrame with datetime index and columns:
                - open, high, low, close, volume
        """
        pass

    @abstractmethod
    async def get_real_time_quote(self, symbol: str) -> Dict:
        """
        Retrieve latest price and metadata (optional).

        Returns:
            Dict with at minimum:
                - price: float
                - timestamp: str (ISO format)
        """
        pass
