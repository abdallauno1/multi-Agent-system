from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_run_returns_events():
    response = client.post(
        "/runs",
        json={
            "goal": "Analyze failed deployment and suggest the next action",
            "context": {
                "service": "payments-api",
                "environment": "staging",
                "error": "CrashLoopBackOff",
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "completed"
    assert len(payload["events"]) >= 6
    assert payload["events"][0]["event_type"] == "PLAN_CREATED"
