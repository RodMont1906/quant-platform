import json
from datetime import datetime
from typing import Optional
from uuid import uuid4

import redis


class AlertManager:
    def __init__(self, redis_url="redis://redis:6379/0"):
        self.redis = redis.Redis.from_url(redis_url)

    def push_alert(
        self, message: str, severity: str = "ERROR", strategy_id: Optional[str] = None
    ):
        alert = {
            "id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "severity": severity,
            "message": message,
            "strategy_id": strategy_id or "UNKNOWN",
        }

        self.redis.rpush("risk_alerts", json.dumps(alert))
        print(f"🚨 Pushed alert to Redis: {alert['message']}")
