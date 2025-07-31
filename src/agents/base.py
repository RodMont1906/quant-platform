# src/agents/base.py
from abc import ABC, abstractmethod
from typing import Any


class AgentBase(ABC):
    def __init__(self, model_type: str, fallback_model: str = None):
        self.model_type = model_type
        self.fallback_model = fallback_model

    @abstractmethod
    def process(self, task: dict) -> dict:
        """Main task execution method"""
        pass

    def get_routing_decision(self, task: dict) -> str:
        """Simple rule-based logic — placeholder for real scoring"""
        if "complexity_score" in task and task["complexity_score"] > 0.7:
            return self.model_type  # e.g., 'gpt-4'
        return self.fallback_model or self.model_type
