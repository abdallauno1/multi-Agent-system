from __future__ import annotations

from fastapi import FastAPI

from app.memory import RunMemory
from app.models import RunRequest
from app.orchestrator import MultiAgentOrchestrator

app = FastAPI(title="Multi-Agent Orchestrator System", version="0.1.0")
memory = RunMemory()
orchestrator = MultiAgentOrchestrator(memory=memory)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/runs")
def list_runs() -> list[dict]:
    return [record.model_dump() for record in memory.all()]


@app.post("/runs")
def create_run(request: RunRequest) -> dict:
    record = orchestrator.run(request)
    return record.model_dump()
