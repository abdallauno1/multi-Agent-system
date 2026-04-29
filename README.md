# Multi-Agent Orchestrator System - Day 2

Day 2 upgrades the project from a simple orchestration loop to an **event-driven runtime** that looks much closer to a real AI platform component.

## What changed in Day 2

- added an **Event Bus** for internal workflow events
- introduced explicit **event types** for plan, execution, validation, retry, and completion
- persisted **event history** in shared memory for each run
- upgraded the orchestrator to use **event-driven handlers**
- added a run lookup endpoint: `GET /runs/{run_id}`
- added extra tests for event flow and API behavior
- added separate docs for architecture, sequence, and Day 2 LinkedIn assets

## Why this matters

This is the transition from:

- demo-style AI orchestration

to:

- **production-style runtime design**
- **decoupled workflow coordination**
- **observable agent execution**
- **replayable event history**

## Architecture at a glance

```text
Client -> FastAPI -> Orchestrator -> Event Bus
                                    |-> Planner
                                    |-> Executor
                                    |-> Validator
                                    |-> Shared Memory
```

## Project Structure

```text
multi-agent-orchestrator-day2/
├── app/
│   ├── agents/
│   │   ├── base.py
│   │   ├── planner.py
│   │   ├── executor.py
│   │   └── validator.py
│   ├── events/
│   │   ├── event_bus.py
│   │   ├── event_types.py
│   │   └── __init__.py
│   ├── main.py
│   ├── memory.py
│   ├── models.py
│   └── orchestrator.py
├── docs/
│   ├── architecture.md
│   ├── overview.md
│   ├── sequence.md
│   └── linkedin-post-day2.md
├── tests/
│   ├── test_api.py
│   └── test_orchestrator.py
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
- Runs: `http://127.0.0.1:8000/runs`

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
    "Incorporate runtime context into the execution strategy",
    "Execute the main action for the goal",
    "Validate the execution result"
  ],
  "events": [
    {"event_type": "PLAN_CREATED", "source": "planner"},
    {"event_type": "TASK_EXECUTE", "source": "orchestrator"},
    {"event_type": "TASK_COMPLETED", "source": "executor"},
    {"event_type": "VALIDATION_REQUEST", "source": "orchestrator"},
    {"event_type": "VALIDATION_PASSED", "source": "validator"},
    {"event_type": "RUN_COMPLETED", "source": "orchestrator"}
  ]
}
```

## Suggested screenshots for Day 2 LinkedIn post

1. `docs/sequence.md`
2. `docs/architecture.md`
3. Swagger UI or `POST /runs` JSON output


