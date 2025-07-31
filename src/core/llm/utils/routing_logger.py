# src/core/llm/utils/routing_logger.py
import logging
from datetime import datetime

logger = logging.getLogger("LLMRouting")


class RoutingLogger:
    def log_model_selection(self, agent: str, task: str, model: str, reason: str):
        logger.info(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "event": "ROUTING_DECISION",
                "agent": agent,
                "task": task,
                "model": model,
                "reason": reason,
            }
        )

    def log_fallback(self, from_model: str, to_model: str, reason: str):
        logger.warning(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "event": "FALLBACK",
                "from_model": from_model,
                "to_model": to_model,
                "reason": reason,
            }
        )

    def log_decision_rationale(self, agent: str, rationale: str, confidence: float):
        logger.info(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "event": "DECISION_LOGIC",
                "agent": agent,
                "confidence": confidence,
                "rationale": rationale,
            }
        )
