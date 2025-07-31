import os
import sys

from dotenv import load_dotenv

# --- Ensure `src/` is in sys.path ---
PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)  # /home/rodri/quant-platform/scripts
SRC_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "..", "src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# --- Load environment variables ---
load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, "..", "deployments", ".env"))

# --- Imports: Drop the `src.` prefix completely ---
import pandas as pd
from sqlalchemy import create_engine

from core.data.validation.data_quality import (check_duplicate_entries,
                                               check_missing_timestamps,
                                               check_price_bounds,
                                               check_volume_anomalies)

# --- Create SQLAlchemy engine ---
engine = create_engine(os.getenv("DATABASE_URL"))

# --- Query recent market data ---
df = pd.read_sql(
    "SELECT * FROM market_data WHERE symbol = 'AAPL' AND timestamp >= NOW() - INTERVAL '2 days'",
    engine,
    parse_dates=["timestamp"],
)
df = df.set_index("timestamp")

# --- Run checks ---
results = {
    **check_missing_timestamps(df),
    **check_price_bounds(df),
    **check_duplicate_entries(df),
    **check_volume_anomalies(df),
}

# --- Report ---
print("Data Quality Report:")
for key, value in results.items():
    print(f"- {key}: {value}")
