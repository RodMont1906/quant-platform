import json
import os

import anthropic

from src.core.llm.providers.base import LLMProvider


class AnthropicProvider(LLMProvider):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def generate_signal(self, market_context, strategy_params):
        prompt = f"""Market context: {market_context}
Strategy parameters: {strategy_params}
Respond only with a valid JSON object like: {{"action": "buy/sell/hold", "confidence": float}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
            )
            raw = response.content[0].text
            result = json.loads(raw)

            if "action" not in result or "confidence" not in result:
                raise ValueError("Malformed Claude response")

        except Exception as e:
            print(f"[AnthropicProvider Error] {e}")
            result = {"action": "hold", "confidence": 0.0}

        return result
