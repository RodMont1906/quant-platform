# src/core/llm/utils/cost_tracker.py
import logging

from tiktoken import encoding_for_model

logger = logging.getLogger("CostTracker")

MODEL_PRICING = {
    "gpt-4": 0.03 / 1000,
    "gpt-4-output": 0.06 / 1000,
    "gpt-3.5": 0.0015 / 1000,
    "gpt-3.5-output": 0.002 / 1000,
    # Extend this as needed for Claude, Ollama, etc.
}


class CostTracker:
    def __init__(self):
        pass

    def count_tokens(self, model: str, text: str) -> int:
        try:
            enc = encoding_for_model(model)
            return len(enc.encode(text))
        except Exception:
            return int(len(text) / 4)  # fallback estimation

    def track(self, model: str, prompt: str, response: str, latency_s: float):
        input_tokens = self.count_tokens(model, prompt)
        output_tokens = self.count_tokens(model, response)

        input_cost = MODEL_PRICING.get(model, 0) * input_tokens
        output_cost = MODEL_PRICING.get(f"{model}-output", 0) * output_tokens
        total_cost = input_cost + output_cost

        logger.info(
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_cost_usd": round(total_cost, 6),
                "latency_seconds": round(latency_s, 3),
            }
        )
