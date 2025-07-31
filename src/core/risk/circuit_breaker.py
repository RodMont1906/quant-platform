import time
from datetime import datetime, timedelta

import redis


class CircuitBreakerTripped(Exception):
    pass


class CircuitBreaker:
    def __init__(self, redis_url="redis://redis:6379/0", key="system_breaker"):
        self.redis = redis.Redis.from_url(redis_url)
        self.key = key

    def trip(self, reason: str, duration_seconds: int = 300):
        expires_at = datetime.utcnow() + timedelta(seconds=duration_seconds)
        self.redis.hset(
            self.key,
            mapping={
                "status": "TRIPPED",
                "reason": reason,
                "expires_at": expires_at.isoformat(),
            },
        )
        print(f"🔴 Circuit breaker TRIPPED for {duration_seconds}s — {reason}")

    def reset(self):
        self.redis.delete(self.key)
        print("🟢 Circuit breaker manually RESET")

    def enforce(self):
        data = self.redis.hgetall(self.key)
        if not data:
            return  # no breaker active

        status = data[b"status"].decode()
        expires_at = datetime.fromisoformat(data[b"expires_at"].decode())

        if status == "TRIPPED":
            if datetime.utcnow() > expires_at:
                self.reset()
            else:
                raise CircuitBreakerTripped(
                    f"🚫 System halted: {data[b'reason'].decode()}"
                )
