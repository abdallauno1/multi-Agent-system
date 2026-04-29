from __future__ import annotations

from app.agents.executor import ExecutorAgent
from app.agents.planner import PlannerAgent
from app.agents.validator import ValidatorAgent
from app.events.event_bus import EventBus
from app.events import event_types as et
from app.memory import RunMemory
from app.models import ExecutionResult, RunEvent, RunRecord, RunRequest, ValidationResult


class MultiAgentOrchestrator:
    def __init__(self, memory: RunMemory | None = None, max_retries: int = 2) -> None:
        self.memory = memory or RunMemory()
        self.max_retries = max_retries
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.validator = ValidatorAgent()
        self.bus = EventBus()
        self._current_record: RunRecord | None = None
        self._subscribe_handlers()

    def _subscribe_handlers(self) -> None:
        self.bus.subscribe(et.PLAN_CREATED, self._on_plan_created)
        self.bus.subscribe(et.TASK_EXECUTE, self._on_task_execute)
        self.bus.subscribe(et.TASK_COMPLETED, self._on_task_completed)
        self.bus.subscribe(et.VALIDATION_REQUEST, self._on_validation_request)
        self.bus.subscribe(et.VALIDATION_PASSED, self._on_validation_passed)
        self.bus.subscribe(et.VALIDATION_FAILED, self._on_validation_failed)

    def _publish(self, event_type: str, payload: dict, source: str) -> RunEvent:
        if self._current_record is None:
            raise RuntimeError("Cannot publish without an active run record")
        return self.bus.publish(
            event_type,
            payload,
            run_id=self._current_record.run_id,
            source=source,
        )

    def _persist_current_record(self) -> None:
        if self._current_record is None:
            raise RuntimeError("No active run to persist")
        self._current_record.events = self.bus.snapshot()
        self.memory.add(self._current_record)

    def run(self, request: RunRequest) -> RunRecord:
        self.bus.reset()
        self._current_record = RunRecord(goal=request.goal, context=request.context, status="planning")

        plan_output = self.planner.run({"goal": request.goal, "context": request.context})
        self._publish(et.PLAN_CREATED, plan_output, source="planner")

        record = self._current_record
        if record is None:
            raise RuntimeError("Run record unexpectedly missing")
        if record.status not in {"completed", "failed"}:
            record.status = "failed"
            record.validation = ValidationResult(
                passed=False,
                reason="Run exited without reaching a terminal event",
            )
            self._persist_current_record()
        return record

    def _on_plan_created(self, event: RunEvent) -> None:
        assert self._current_record is not None
        self._current_record.plan = event.payload["steps"]
        self._current_record.status = "executing"
        self._publish(
            et.TASK_EXECUTE,
            {
                "goal": self._current_record.goal,
                "context": self._current_record.context,
                "attempt": 1,
                "plan": self._current_record.plan,
            },
            source="orchestrator",
        )

    def _on_task_execute(self, event: RunEvent) -> None:
        assert self._current_record is not None
        self._current_record.status = "executing"
        self._current_record.attempts = int(event.payload.get("attempt", 1))
        execution_output = self.executor.run(event.payload)
        self._publish(et.TASK_COMPLETED, execution_output, source="executor")

    def _on_task_completed(self, event: RunEvent) -> None:
        assert self._current_record is not None
        self._current_record.result = ExecutionResult(
            summary=event.payload["summary"],
            next_action=event.payload["next_action"],
            confidence=event.payload["confidence"],
            details=event.payload.get("details", {}),
        )
        self._current_record.status = "validating"
        self._publish(
            et.VALIDATION_REQUEST,
            {
                **self._current_record.result.model_dump(),
                "attempt": self._current_record.attempts,
            },
            source="orchestrator",
        )

    def _on_validation_request(self, event: RunEvent) -> None:
        validation_output = self.validator.run(event.payload)
        event_type = et.VALIDATION_PASSED if validation_output["passed"] else et.VALIDATION_FAILED
        self._publish(event_type, validation_output, source="validator")

    def _on_validation_passed(self, event: RunEvent) -> None:
        assert self._current_record is not None
        self._current_record.validation = ValidationResult(
            passed=event.payload["passed"],
            reason=event.payload["reason"],
        )
        self._current_record.status = "completed"
        self._publish(et.RUN_COMPLETED, {"status": "completed"}, source="orchestrator")
        self._persist_current_record()

    def _on_validation_failed(self, event: RunEvent) -> None:
        assert self._current_record is not None
        self._current_record.validation = ValidationResult(
            passed=event.payload["passed"],
            reason=event.payload["reason"],
        )
        next_attempt = self._current_record.attempts + 1
        if next_attempt <= self.max_retries + 1:
            self._current_record.status = "retrying"
            self._publish(
                et.TASK_EXECUTE,
                {
                    "goal": self._current_record.goal,
                    "context": self._current_record.context,
                    "attempt": next_attempt,
                    "plan": self._current_record.plan,
                },
                source="orchestrator",
            )
            return

        self._current_record.status = "failed"
        self._publish(et.RUN_FAILED, {"status": "failed"}, source="orchestrator")
        self._persist_current_record()