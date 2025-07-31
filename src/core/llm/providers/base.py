from abc import ABC, abstractmethod
from typing import Dict


class LLMProvider(ABC):
    @abstractmethod
    async def generate_signal(
        self, market_context: Dict, strategy_params: Dict
    ) -> Dict:
        pass
