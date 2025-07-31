from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List


class ExposureViolation(Exception):
    pass


@dataclass
class EnrichedPosition:
    symbol: str
    quantity: Decimal
    price: Decimal
    sector: str
    country: str


@dataclass
class EnrichedPortfolio:
    positions: List[EnrichedPosition]
    total_value: Decimal


class ExposureGuard:
    def __init__(self, max_sector_pct=0.30, max_country_pct=0.50):
        self.max_sector_pct = Decimal(str(max_sector_pct))
        self.max_country_pct = Decimal(str(max_country_pct))

    def enforce(self, portfolio: EnrichedPortfolio):
        sector_exposure: Dict[str, Decimal] = defaultdict(Decimal)
        country_exposure: Dict[str, Decimal] = defaultdict(Decimal)

        for pos in portfolio.positions:
            value = pos.quantity * pos.price
            sector_exposure[pos.sector] += value
            country_exposure[pos.country] += value

        for sector, value in sector_exposure.items():
            ratio = value / portfolio.total_value
            if ratio > self.max_sector_pct:
                raise ExposureViolation(
                    f"Sector '{sector}' exposure {ratio:.2%} exceeds {self.max_sector_pct:.0%} limit."
                )

        for country, value in country_exposure.items():
            ratio = value / portfolio.total_value
            if ratio > self.max_country_pct:
                raise ExposureViolation(
                    f"Country '{country}' exposure {ratio:.2%} exceeds {self.max_country_pct:.0%} limit."
                )

        return True
