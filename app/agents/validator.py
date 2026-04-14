from __future__ import annotations

from typing import Any, Dict

from app.agents.base import BaseAgent


class ValidatorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="validator")

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        summary = payload.get("summary", "")
        next_action = payload.get("next_action", "")
        confidence = float(payload.get("confidence", 0.0))

        passed = bool(summary and next_action and confidence >= 0.70)
        reason = (
            "Result contains a summary and actionable next action"
            if passed
            else "Result is incomplete or confidence is too low"
        )

        return {
            "agent": self.name,
            "passed": passed,
            "reason": reason,
        }
