# src/core/data/providers/fallback.py

from typing import Dict, List

import pandas as pd

from core.data.providers.base import MarketDataProvider


class FallbackMarketDataProvider(MarketDataProvider):
    def __init__(self, providers: List[MarketDataProvider]):
        if not providers:
            raise ValueError(
                "At least one provider must be passed to FallbackMarketDataProvider"
            )
        self.providers = providers

    async def get_historical_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        last_error = None
        for provider in self.providers:
            try:
                return await provider.get_historical_data(
                    symbol, start_date, end_date, interval
                )
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(f"All fallback providers failed. Last error: {last_error}")

    async def get_real_time_quote(self, symbol: str) -> Dict:
        last_error = None
        for provider in self.providers:
            try:
                return await provider.get_real_time_quote(symbol)
            except NotImplementedError:
                continue
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(
            f"All fallback providers failed for real-time quote. Last error: {last_error}"
        )
