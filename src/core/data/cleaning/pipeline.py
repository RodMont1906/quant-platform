# src/core/data/cleaning/pipeline.py
import pandas as pd

from .cleaner import DataCleaner
from .validator import DataValidator


class DataPipeline:
    def __init__(self):
        self.validator = DataValidator()
        self.cleaner = DataCleaner()

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        valid_df = self.validator.validate(df)
        return self.cleaner.clean(valid_df)
