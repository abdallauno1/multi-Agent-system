from app.memory import RunMemory
from app.models import RunRequest
from app.orchestrator import MultiAgentOrchestrator


def test_orchestrator_completes_run(tmp_path):
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
