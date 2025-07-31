# src/core/llm/agents/base.py
from abc import ABC, abstractmethod


class Task:
    def __init__(
        self, prompt: str, complexity_score: float = 0.5, task_id: str = "unknown"
    ):
        self.prompt = prompt
        self.complexity_score = complexity_score
        self.task_id = task_id


class Response:
    def __init__(
        self, response: str, confidence: float, tokens_used: int = 0, error: str = None
    ):
        self.response = response
        self.confidence = confidence
        self.tokens_used = tokens_used
        self.error = error


class ModelChoice:
    def __init__(self, model: str, reason: str):
        self.model = model
        self.reason = reason


class AgentBase(ABC):
    def __init__(self, model_type: str, fallback_model: str = None):
        self.model_type = model_type
        self.fallback_model = fallback_model

    @abstractmethod
    def process(self, task: Task) -> Response:
        pass

    def get_routing_decision(self, task: Task) -> ModelChoice:
        if task.complexity_score > 0.7:
            return ModelChoice("gpt-4", "High complexity task")
        return ModelChoice("llama3", "Low complexity task")
