from __future__ import annotations

from typing import Any, Dict

from app.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="planner")

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        goal = payload["goal"]
        context = payload.get("context", {})

        steps = [
            "Understand the goal and available context",
            "Execute the main action for the goal",
            "Validate the execution result",
        ]

        if context:
            steps.insert(1, "Incorporate runtime context into the execution strategy")

        return {
            "agent": self.name,
            "goal": goal,
            "steps": steps,
        }
