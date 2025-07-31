from typing import Dict, Tuple

import pandas as pd


class PerformanceAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.sort_index()

    def compute_cumulative_return(self) -> float:
        return self.df["pnl"].cumsum().iloc[-1]

    def compute_max_drawdown(self) -> float:
        cumulative = self.df["pnl"].cumsum()
        peak = cumulative.cummax()
        drawdown = cumulative - peak
        return drawdown.min()

    def compute_symbol_attribution(self) -> Dict[str, float]:
        return self.df.groupby("symbol")["pnl"].sum().to_dict()
