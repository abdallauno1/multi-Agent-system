from __future__ import annotations

from typing import Any, Dict

from app.agents.base import BaseAgent
from app.llm.client import LLMClient, get_llm_client
from app.prompts.templates import VALIDATOR_SYSTEM_PROMPT


class ValidatorAgent(BaseAgent):
    def __init__(self, llm: LLMClient | None = None) -> None:
        super().__init__(name="validator")
        self.llm = llm or get_llm_client()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        attempt = int(payload.get("attempt", 1))

        response = self.llm.complete_json(
            system_prompt=VALIDATOR_SYSTEM_PROMPT,
            user_payload={
                "task": "validate",
                **payload,
            },
        )

        passed = bool(response.get("passed", False))
        reason = response.get("reason") or (
            "Result contains a summary and actionable next action"
            if passed
            else "Result is incomplete or confidence is too low; retry required"
        )

        return {
            "agent": self.name,
            "passed": passed,
            "reason": reason,
            "llm_provider": self.llm.provider_name,
            "attempt": attempt,
        }
