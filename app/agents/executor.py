from __future__ import annotations

from typing import Any, Dict

from app.agents.base import BaseAgent


class ExecutorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="executor")

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        goal = payload["goal"]
        context = payload.get("context", {})
        attempt = payload.get("attempt", 1)

        service = context.get("service", "unknown-service")
        environment = context.get("environment", "unknown-env")
        error = context.get("error")

        next_action = "Break the goal into smaller operational checks"
        confidence = 0.64 if attempt == 1 and not error else 0.84
        if error:
            next_action = f"Inspect logs for {service} in {environment} and compare with latest deployment changes"
        elif attempt > 1:
            next_action = f"Review telemetry and rollback signals for {service} in {environment}"

        return {
            "agent": self.name,
            "summary": f"Executed task for goal: {goal}",
            "next_action": next_action,
            "confidence": confidence,
            "details": {
                "service": service,
                "environment": environment,
                "error": error,
                "attempt": attempt,
            },
        }
