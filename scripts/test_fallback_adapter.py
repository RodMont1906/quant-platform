# scripts/test_fallback_adapter.py

import os

from dotenv import load_dotenv

load_dotenv()

import asyncio
from datetime import date

import pandas as pd

from core.data.providers.fallback import FallbackMarketDataProvider
from core.data.providers.polygon import PolygonFreeAdapter
from core.data.providers.yahoo import YahooFinanceAdapter


async def main():
    polygon = PolygonFreeAdapter()
    yahoo = YahooFinanceAdapter()

    fallback = FallbackMarketDataProvider([polygon, yahoo])

    symbol = "AAPL"
    start_date = "2024-01-01"
    end_date = "2024-06-30"
    interval = "1d"

    print(f"Fetching {interval} OHLCV data for {symbol} using Fallback Provider...")
    try:
        df: pd.DataFrame = await fallback.get_historical_data(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
        )
        print(df.head(10))
        print("\nColumns:", df.columns)
        print("\nData types:\n", df.dtypes)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
