# src/core/llm/schema/base.py
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ModelChoice(str, Enum):
    GPT4 = "gpt-4"
    LLAMA3 = "llama3:latest"


class Task(BaseModel):
    prompt: str
    complexity_score: float = 0.5
    task_id: str = "default"


class LLMResponse(BaseModel):
    response: str
    tokens_used: int = 0
    confidence: float = 0.0
    error: Optional[str] = None
