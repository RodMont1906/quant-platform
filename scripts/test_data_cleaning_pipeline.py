# scripts/test_data_cleaning_pipeline.py
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath("src"))
from core.data.cleaning.pipeline import DataPipeline

raw_data = pd.DataFrame(
    {
        "open": [100, 105, None, 180],
        "high": [110, 107, 150, 200],
        "low": [95, 103, 140, 170],
        "close": [108, 106, 148, 300],  # Huge jump here
        "volume": [1000, 0, 1500, 2000],
    },
    index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]),
)

pipeline = DataPipeline()
cleaned = pipeline.run(raw_data)

print(cleaned)
