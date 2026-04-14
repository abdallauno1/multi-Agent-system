from __future__ import annotations

from app.agents.executor import ExecutorAgent
from app.agents.planner import PlannerAgent
from app.agents.validator import ValidatorAgent
from app.memory import RunMemory
from app.models import ExecutionResult, RunRecord, RunRequest, ValidationResult


class MultiAgentOrchestrator:
    def __init__(self, memory: RunMemory | None = None, max_retries: int = 2) -> None:
        self.memory = memory or RunMemory()
        self.max_retries = max_retries
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.validator = ValidatorAgent()

    def run(self, request: RunRequest) -> RunRecord:
        record = RunRecord(goal=request.goal, context=request.context, status="planning")

        plan_output = self.planner.run({"goal": request.goal, "context": request.context})
        record.plan = plan_output["steps"]

        for attempt in range(1, self.max_retries + 2):
            record.status = "executing"
            record.attempts = attempt

            execution_output = self.executor.run(
                {
                    "goal": request.goal,
                    "context": request.context,
                    "attempt": attempt,
                }
            )
            result = ExecutionResult(
                summary=execution_output["summary"],
                next_action=execution_output["next_action"],
                confidence=execution_output["confidence"],
                details=execution_output.get("details", {}),
            )
            record.result = result

            record.status = "validating"
            validation_output = self.validator.run(result.model_dump())
            validation = ValidationResult(
                passed=validation_output["passed"],
                reason=validation_output["reason"],
            )
            record.validation = validation

            if validation.passed:
                record.status = "completed"
                self.memory.add(record)
                return record

        record.status = "failed"
        self.memory.add(record)
        return record
