# src/core/data/providers/polygon.py

import os
from datetime import datetime
from typing import Dict

import httpx
import pandas as pd

from core.data.providers.base import MarketDataProvider  # ✅ FIXED IMPORT


class PolygonFreeAdapter(MarketDataProvider):
    BASE_URL = "https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_}/{to}"

    def __init__(self):
        self.api_key = os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise ValueError("Missing POLYGON_API_KEY in environment variables")

    async def get_historical_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        interval_map = {
            "1d": (1, "day"),
            "1h": (1, "hour"),
            "15m": (15, "minute"),
        }

        if interval not in interval_map:
            raise ValueError(f"Unsupported interval: {interval}")

        multiplier, timespan = interval_map[interval]

        url = self.BASE_URL.format(
            symbol=symbol.upper(),
            multiplier=multiplier,
            timespan=timespan,
            from_=start_date,
            to=end_date,
        )

        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 5000,
            "apiKey": self.api_key,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            if response.status_code != 200:
                raise RuntimeError(
                    f"Polygon API error: {response.status_code} {response.text}"
                )

            data = response.json().get("results", [])
            if not data:
                raise ValueError("No data returned from Polygon")

            df = pd.DataFrame(data)
            df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
            df.set_index("timestamp", inplace=True)

            df.rename(
                columns={
                    "o": "open",
                    "h": "high",
                    "l": "low",
                    "c": "close",
                    "v": "volume",
                },
                inplace=True,
            )

            return df[["open", "high", "low", "close", "volume"]]

    async def get_real_time_quote(self, symbol: str) -> Dict:
        raise NotImplementedError("Real-time quotes not available in free tier.")
