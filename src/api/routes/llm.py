# src/api/routes/llm.py
import logging

from fastapi import APIRouter, HTTPException

from src.agents.llm_orchestrator import LLMOrchestrator
from src.core.llm.schema.base import LLMResponse, Task

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/test", response_model=LLMResponse)
async def test_llm(task: Task):
    try:
        orchestrator = LLMOrchestrator()
        result = orchestrator.run_task(task)
        return result
    except Exception as e:
        logger.error(f"LLM API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")


@router.get("/health")
async def llm_health():
    try:
        orchestrator = LLMOrchestrator()
        result = orchestrator.run_task(
            Task(
                prompt="Say OK if you can hear me",
                complexity_score=0.3,
                task_id="health_check",
            )
        )
        return {
            "status": "healthy" if result.confidence > 0 else "degraded",
            "ollama_available": "OK" in result.response,
            "result": result,
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
