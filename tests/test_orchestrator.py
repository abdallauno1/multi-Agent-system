from app.memory import RunMemory
from app.models import RunRequest
from app.orchestrator import MultiAgentOrchestrator


def test_orchestrator_completes_run_and_persists_event_history(tmp_path):
    memory = RunMemory(path=str(tmp_path / "runs.json"))
    orchestrator = MultiAgentOrchestrator(memory=memory)

    request = RunRequest(
        goal="Analyze failed deployment and suggest the next action",
        context={
            "service": "payments-api",
            "environment": "staging",
            "error": "CrashLoopBackOff",
        },
    )

    record = orchestrator.run(request)

    assert record.status == "completed"
    assert record.validation is not None
    assert record.validation.passed is True
    assert record.result is not None
    assert "Inspect logs" in record.result.next_action
    assert len(record.events) >= 6
    assert record.events[0].event_type == "PLAN_CREATED"
    assert record.events[-1].event_type == "RUN_COMPLETED"


def test_orchestrator_retries_before_success(tmp_path):
    memory = RunMemory(path=str(tmp_path / "runs.json"))
    orchestrator = MultiAgentOrchestrator(memory=memory)

    request = RunRequest(
        goal="Review production incident and propose a mitigation plan",
        context={
            "service": "orders-api",
            "environment": "prod",
        },
    )

    record = orchestrator.run(request)

    assert record.status == "completed"
    assert record.attempts == 2
    assert sum(1 for event in record.events if event.event_type == "TASK_EXECUTE") == 2
    assert sum(1 for event in record.events if event.event_type == "VALIDATION_FAILED") == 1
    assert record.events[-1].event_type == "RUN_COMPLETED"
