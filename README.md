# Multi-Agent Orchestrator System - Day 1

A production-style Day 1 foundation for a multi-agent system with:

- **Planner Agent**: converts a user goal into executable steps
- **Executor Agent**: executes steps with retry support
- **Validator Agent**: reviews outputs and decides pass/fail
- **Orchestrator**: manages flow between agents
- **Shared Memory**: simple in-memory and persisted run history
- **FastAPI API**: endpoint to start a workflow
- **Tests**: basic orchestration coverage

## Why this project

This repo is designed to look like a real platform engineering / AI systems project, not a toy chatbot. It demonstrates:

- agent roles
- task delegation
- shared memory
- validation loops
- retries and fallback behavior
- API-first architecture

## Day 1 Scope

Day 1 focuses on the **core orchestration foundation**.

Done today:

- project scaffold
- FastAPI service
- planner / executor / validator agents
- orchestrator with retry loop
- run memory persistence
- architecture docs
- GitHub-ready structure
- LinkedIn-ready markdown diagram

Planned next:

- **Day 2**: async tasks, queue/event support, Docker Compose, observability basics
- **Day 3**: Kubernetes manifests, Prometheus metrics, GitHub Actions polish, demo video assets

## Project Structure

```text
multi-agent-orchestrator-day1/
├── app/
│   ├── agents/
│   │   ├── base.py
│   │   ├── planner.py
│   │   ├── executor.py
│   │   └── validator.py
│   ├── main.py
│   ├── memory.py
│   ├── models.py
│   └── orchestrator.py
├── docs/
│   ├── architecture.md
│   └── linkedin-post-day1.md
├── tests/
│   └── test_orchestrator.py
├── .github/workflows/ci.yml
├── .gitignore
├── Dockerfile
├── Makefile
├── requirements.txt
└── README.md
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/runs \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Analyze failed deployment and suggest the next action",
    "context": {
      "service": "payments-api",
      "environment": "staging",
      "error": "CrashLoopBackOff"
    }
  }'
```

## Example Response

```json
{
  "run_id": "...",
  "status": "completed",
  "attempts": 1,
  "plan": [
    "Understand the goal and available context",
    "Execute the main action for the goal",
    "Validate the execution result"
  ],
  "result": {
    "summary": "Executed task for goal: Analyze failed deployment and suggest the next action",
    "next_action": "Inspect pod logs and recent deployment diff",
    "confidence": 0.84
  },
  "validation": {
    "passed": true,
    "reason": "Result contains a summary and actionable next action"
  }
}
```
  