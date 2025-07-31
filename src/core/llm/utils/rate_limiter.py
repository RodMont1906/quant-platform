# src/core/llm/utils/rate_limiter.py
import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.calls = defaultdict(list)  # model/provider name → list[timestamps]

    def check(self, provider: str):
        now = time.time()
        window_start = now - self.window_seconds
        self.calls[provider] = [t for t in self.calls[provider] if t > window_start]

        if len(self.calls[provider]) >= self.max_requests:
            raise Exception(
                f"[RateLimiter] {provider} exceeded {self.max_requests} reqs/{self.window_seconds}s"
            )

        self.calls[provider].append(now)
