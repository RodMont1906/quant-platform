from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Position:
    symbol: str
    quantity: Decimal
    price: Decimal  # current market price


@dataclass
class Portfolio:
    positions: List[Position]
    total_value: Decimal
    daily_pnl: Decimal


@dataclass
class RiskConfig:
    max_position_pct: float = 0.10  # 10%
    max_daily_loss_pct: float = 0.02  # 2%
    max_drawdown_pct: float = 0.15  # 15%
    correlation_threshold: float = 0.7  # for future extension


class RiskViolation(Exception):
    pass


class RiskManager:
    def __init__(self, config: RiskConfig):
        self.config = config

    def validate_trade(self, trade: Position, portfolio: Portfolio):
        position_value = trade.quantity * trade.price
        max_allowed = portfolio.total_value * Decimal(self.config.max_position_pct)

        if position_value > max_allowed:
            raise RiskViolation(
                f"Position size {position_value} exceeds limit {max_allowed}."
            )

        if portfolio.daily_pnl < -portfolio.total_value * Decimal(
            self.config.max_daily_loss_pct
        ):
            raise RiskViolation(f"Daily loss {portfolio.daily_pnl} exceeds limit.")

        # future: validate correlation across positions

        return True

    def compute_portfolio_risk(self, portfolio: Portfolio) -> dict:
        risk_exposures = {}
        for pos in portfolio.positions:
            exposure_pct = (pos.quantity * pos.price) / portfolio.total_value
            risk_exposures[pos.symbol] = float(exposure_pct)
        return risk_exposures
