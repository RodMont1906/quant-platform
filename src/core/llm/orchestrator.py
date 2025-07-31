import asyncio
# from src.core.llm.providers.anthropic import AnthropicProvider  # Optional fallback
from typing import Dict

from src.core.llm.providers.openai import OpenAIProvider


class LLMOrchestrator:
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider(),
            # "anthropic": AnthropicProvider()  # Uncomment if/when Claude API is enabled
        }

    async def generate_trading_signal(
        self, market_context: Dict, strategy_params: Dict, confidence_threshold=0.7
    ) -> Dict:
        responses = await asyncio.gather(
            *[
                provider.generate_signal(market_context, strategy_params)
                for provider in self.providers.values()
            ]
        )

        avg_conf = sum(r["confidence"] for r in responses) / len(responses)
        if avg_conf >= confidence_threshold:
            actions = [r["action"] for r in responses]
            consensus = max(set(actions), key=actions.count)
            return {"action": consensus, "confidence": avg_conf}
        else:
            return {"action": "hold", "confidence": avg_conf}
