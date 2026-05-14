from __future__ import annotations

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.memory import RunMemory
from app.models import RunRequest
from app.orchestrator import MultiAgentOrchestrator

app = FastAPI(title="Multi-Agent Orchestrator System", version="0.3.0")
memory = RunMemory()
orchestrator = MultiAgentOrchestrator(memory=memory)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": app.version}


@app.get("/ready")
def ready() -> dict:
    return {"status": "ready", "memory_records": len(memory.all())}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/runs")
def list_runs() -> list[dict]:
    return [record.model_dump() for record in memory.all()]


@app.get("/runs/{run_id}")
def get_run(run_id: str) -> dict:
    record = memory.get(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return record.model_dump()


@app.post("/runs")
def create_run(request: RunRequest) -> dict:
    record = orchestrator.run(request)
    return record.model_dump()
