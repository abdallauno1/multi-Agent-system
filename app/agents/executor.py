from __future__ import annotations

from typing import Any, Dict

from app.agents.base import BaseAgent
from app.llm.client import LLMClient, get_llm_client
from app.prompts.templates import EXECUTOR_SYSTEM_PROMPT


class ExecutorAgent(BaseAgent):
    def __init__(self, llm: LLMClient | None = None) -> None:
        super().__init__(name="executor")
        self.llm = llm or get_llm_client()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        goal = payload["goal"]
        context = payload.get("context", {})
        attempt = payload.get("attempt", 1)

        response = self.llm.complete_json(
            system_prompt=EXECUTOR_SYSTEM_PROMPT,
            user_payload={
                "task": "execute",
                "goal": goal,
                "context": context,
                "attempt": attempt,
                "plan": payload.get("plan", []),
            },
        )

        service = context.get("service", "unknown-service")
        environment = context.get("environment", "unknown-env")
        error = context.get("error")

        details = response.get("details", {}) or {}
        details.update(
            {
                "service": service,
                "environment": environment,
                "error": error,
                "attempt": attempt,
                "llm_provider": self.llm.provider_name,
            }
        )

        next_action = response.get("next_action") or "Break the goal into smaller operational checks"
        if error and "Inspect logs" not in next_action:
            next_action = f"Inspect logs for {service} in {environment} and compare with latest deployment changes"

        return {
            "agent": self.name,
            "summary": response.get("summary") or f"Executed task for goal: {goal}",
            "next_action": next_action,
            "confidence": float(response.get("confidence", 0.64 if attempt == 1 and not error else 0.84)),
            "details": details,
        }
