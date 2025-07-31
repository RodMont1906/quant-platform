# src/agents/llm_orchestrator.py
import time

from src.core.llm.providers.ollama_provider import OllamaProvider
from src.core.llm.schema.base import LLMResponse, ModelChoice, Task
from src.core.llm.utils.cost_tracker import CostTracker
from src.core.llm.utils.rate_limiter import RateLimiter
from src.core.llm.utils.routing_logger import RoutingLogger


# Dummy OpenAI mock
class OpenAIProvider:
    def generate(self, prompt: str) -> LLMResponse:
        return LLMResponse(
            response=f"OpenAI response: {prompt}",
            tokens_used=100,
            confidence=0.5,  # Low to trigger fallback
        )


class LLMOrchestrator:
    def __init__(self):
        self.providers = {
            ModelChoice.GPT4: OpenAIProvider(),
            ModelChoice.LLAMA3: OllamaProvider(model_type=ModelChoice.LLAMA3.value),
        }
        self.rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
        self.cost_tracker = CostTracker()
        self.logger = RoutingLogger()

    def run_task(self, task: Task) -> LLMResponse:
        model_choice = (
            ModelChoice.GPT4 if task.complexity_score > 0.7 else ModelChoice.LLAMA3
        )

        self.logger.log_model_selection(
            agent="GenericAgent",
            task=task.task_id,
            model=model_choice.value,
            reason=f"complexity_score={task.complexity_score}",
        )

        try:
            self.rate_limiter.check(model_choice.value)
            start = time.time()

            if model_choice == ModelChoice.LLAMA3:
                result = self.providers[model_choice].process(task)
            else:
                result = self.providers[model_choice].generate(task.prompt)

            latency = time.time() - start
            self.cost_tracker.track(
                model_choice.value, task.prompt, result.response, latency
            )

            if result.confidence < 0.75:
                raise RuntimeError("Low confidence — fallback triggered")

            self.logger.log_decision_rationale(
                "GenericAgent", result.response, result.confidence
            )
            return result

        except Exception as e:
            fallback_model = (
                ModelChoice.LLAMA3
                if model_choice != ModelChoice.LLAMA3
                else ModelChoice.GPT4
            )

            self.logger.log_fallback(
                model_choice.value, fallback_model.value, reason=str(e)
            )

            try:
                fallback_task = Task(
                    prompt=f"[Fallback] {task.prompt}",
                    complexity_score=task.complexity_score,
                    task_id=f"{task.task_id}_fallback",
                )

                if fallback_model == ModelChoice.LLAMA3:
                    fallback_result = self.providers[fallback_model].process(
                        fallback_task
                    )
                else:
                    fallback_result = self.providers[fallback_model].generate(
                        fallback_task.prompt
                    )

                latency = time.time() - start
                self.cost_tracker.track(
                    fallback_model.value,
                    fallback_task.prompt,
                    fallback_result.response,
                    latency,
                )
                self.logger.log_decision_rationale(
                    "GenericAgent-Fallback",
                    fallback_result.response,
                    fallback_result.confidence,
                )
                return fallback_result

            except Exception as final_fail:
                return LLMResponse(
                    response="All providers failed",
                    confidence=0.0,
                    error=str(final_fail),
                )
