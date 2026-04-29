from __future__ import annotations

from typing import Any, Dict

from app.agents.base import BaseAgent


class ValidatorAgent:
    def run(self, payload):
        attempt = payload.get("attempt", 1)

        # forza fallimento al primo tentativo
        if attempt == 1:
            return {
                "passed": False,
                "reason": "Initial attempt not sufficient"
            }

        # secondo tentativo passa
        return {
            "passed": True,
            "reason": "Result is acceptable"
        }
