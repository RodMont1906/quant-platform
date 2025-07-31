# src/core/llm/providers/ollama_provider.py
import logging
import os

import requests
from dotenv import load_dotenv

from src.agents.base import AgentBase
from src.core.llm.schema.base import LLMResponse, Task

logger = logging.getLogger("LLMRouting")

load_dotenv()


class OllamaProvider(AgentBase):
    def __init__(self, model_type: str = "llama3:latest", fallback_model: str = None):
        super().__init__(model_type, fallback_model)
        self.api_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def process(self, task: Task) -> LLMResponse:
        payload = {"model": self.model_type, "prompt": task.prompt, "stream": False}

        url = f"{self.api_url}/api/generate"
        logger.info(f"🟢 Sending prompt to Ollama → {url}")

        try:
            res = requests.post(url, json=payload, timeout=60)
            res.raise_for_status()
            data = res.json()
            return LLMResponse(
                response=data.get("response", ""),
                tokens_used=data.get("eval_count", 0),
                confidence=0.9,
            )
        except Exception as e:
            logger.error(f"❌ OllamaProvider failed: {e}")
            return LLMResponse(
                response="Ollama call failed", confidence=0.0, error=str(e)
            )
