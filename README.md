# 🚀 Multi-Agent Orchestrator System

A production-style multi-agent system evolving across 3 days:

- **Day 1:** core multi-agent orchestration
- **Day 2:** event-driven runtime
- **Day 3:** Kubernetes + observability

This project is focused on building an AI platform component, not a simple chatbot demo.

---

## 🧠 Project Vision

Design and build a realistic AI agent runtime using concepts from:

- AI Agents
- Platform Engineering
- Event-Driven Architecture
- Kubernetes
- Observability
- SRE-style reliability patterns

---

# 🥇 Day 1 — Core Multi-Agent System

## What was built

- Planner Agent creates an execution plan
- Executor Agent executes the task
- Validator Agent validates the result
- Orchestrator manages the workflow
- retry loop based on validation
- shared memory persistence
- FastAPI API layer

## Day 1 Flow

```text
Client -> FastAPI -> Orchestrator
        -> Planner -> Executor -> Validator
        -> Retry if validation fails
        -> Persist result
```

---

# 🥈 Day 2 — Event-Driven Architecture

Day 2 evolved the system from direct synchronous calls to event-driven coordination.

## What changed

- Event Bus implementation
- explicit event types
- decoupled agents
- event-based retry flow
- event history stored for every run
- run lookup endpoint: `GET /runs/{run_id}`

## Events

- `PLAN_CREATED`
- `TASK_EXECUTE`
- `TASK_COMPLETED`
- `VALIDATION_REQUEST`
- `VALIDATION_PASSED`
- `VALIDATION_FAILED`
- `RUN_COMPLETED`
- `RUN_FAILED`

## Day 2 Flow

```text
Client -> FastAPI -> Orchestrator -> Event Bus
                                    |-> Planner
                                    |-> Executor
                                    |-> Validator
                                    |-> Shared Memory
```

---

# 🥉 Day 3 — Kubernetes + Observability

Day 3 turns the event-driven runtime into a production-style platform component.

## What was added

- Docker runtime
- Docker Compose stack
- Prometheus metrics endpoint: `/metrics`
- Grafana dashboard provisioning
- Kubernetes manifests
- readiness endpoint: `/ready`
- liveness endpoint: `/health`
- structured JSON logs
- observability tests

## Metrics

The API exposes Prometheus metrics for:

- total runs by status
- total events by event type and source
- agent execution latency
- end-to-end run duration
- active runs

---

# 🛠️ Tech Stack

- Python
- FastAPI
- Pydantic
- Prometheus client
- Grafana
- Docker
- Kubernetes
- Pytest

---

# ▶️ Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`
- Ready: `http://127.0.0.1:8000/ready`
- Metrics: `http://127.0.0.1:8000/metrics`

---

# 🐳 Run with Docker Compose

```bash
docker compose up --build
```

Open:

- API: `http://localhost:8000/docs`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

Grafana login:

- username: `admin`
- password: `admin`

---

# ☸️ Deploy to Kubernetes

Build the local image:

```bash
docker build -t multi-agent-orchestrator:day3 .
```

Apply manifests:

```bash
kubectl apply -k k8s/
```

Check resources:

```bash
kubectl get all -n multi-agent-system
```

Port-forward:

```bash
kubectl port-forward svc/multi-agent-orchestrator -n multi-agent-system 8000:80
```

Open:

```text
http://localhost:8000/docs
```

---

# 🧪 Tests

```bash
pytest
```





# 🧪 Example Request

```bash
curl -X POST http://127.0.0.1:8000/runs \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Review production incident and propose a mitigation plan",
    "context": {
      "service": "orders-api",
      "environment": "prod"
    }
  }'
```

---

# 📈 Roadmap

Next improvements:

- Helm chart
- OpenTelemetry tracing
- Redis or Kafka-backed event bus
- persistent storage
- CI/CD deployment pipeline

---

# 💡 Why this project

This project demonstrates how AI agents can be treated as platform workloads:

- orchestrated
- event-driven
- observable
- deployable
- testable

The goal is to move from AI demos to real AI Platform Engineering.
