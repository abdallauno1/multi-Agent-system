from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ready_endpoint():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_metrics_endpoint_exposes_prometheus_metrics():
    client.post(
        "/runs",
        json={
            "goal": "Review production incident and propose a mitigation plan",
            "context": {"service": "orders-api", "environment": "prod"},
        },
    )

    response = client.get("/metrics")

    assert response.status_code == 200
    assert "multi_agent_runs_total" in response.text
    assert "multi_agent_events_total" in response.text
