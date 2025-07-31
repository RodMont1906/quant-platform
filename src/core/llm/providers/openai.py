import json
import os

from openai import OpenAI

from src.core.llm.providers.base import LLMProvider
from src.core.llm.utils.cost_tracker import CostTracker
from src.core.llm.utils.rate_limiter import RateLimiter

rate_limiter = RateLimiter()
cost_tracker = CostTracker()


class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def generate_signal(self, market_context, strategy_params):
        if not rate_limiter.allow("openai"):
            raise Exception("Rate limit exceeded for OpenAI")

        prompt = f"""Market context: {market_context}
Strategy parameters: {strategy_params}
Respond only with a valid JSON object like: {{"action": "buy/sell/hold", "confidence": float}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )

            raw = response.choices[0].message.content
            usage = response.usage
            cost_tracker.log_cost(
                "openai", usage.prompt_tokens, usage.completion_tokens
            )

            result = json.loads(raw)
            if "action" not in result or "confidence" not in result:
                raise ValueError("Malformed LLM response")

        except Exception as e:
            print(f"[OpenAIProvider Error] {e}")
            result = {"action": "hold", "confidence": 0.0}

        return result
