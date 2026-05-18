# 🚀 Multi-Agent Orchestrator System

A production-style multi-agent system evolving across 4 days:

- **Day 1:** core multi-agent orchestration
- **Day 2:** event-driven runtime
- **Day 3:** Kubernetes + observability
- **Day 4:** LLM-powered agents with provider abstraction

This project is focused on building an AI platform component, not a simple chatbot demo.

---

## 🧠 Project Vision

Design and build a realistic AI agent runtime using concepts from:

- AI Agents
- LLM-powered reasoning
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

# 🏁 Day 4 — LLM-Powered Agents

Day 4 upgrades the agents from deterministic logic to an LLM-powered design while keeping the project safe for local development and CI.

## What was added

- LLM provider abstraction
- mock provider for deterministic local execution
- OpenAI-compatible provider support
- Ollama provider support for local LLMs
- prompt templates for Planner, Executor, and Validator
- LLM-generated planning
- LLM-assisted execution output
- LLM-based validation and retry decision

## Provider Modes

```text
LLM_PROVIDER=mock    -> deterministic local behavior, CI-safe
LLM_PROVIDER=openai  -> OpenAI-compatible chat completions API
LLM_PROVIDER=ollama  -> local Ollama model via /api/generate
```

Default mode:

```bash
LLM_PROVIDER=mock
```

This means the project runs without external API keys by default.

---

# 🛠️ Tech Stack

- Python
- FastAPI
- Pydantic
- Custom Event Bus
- LLM provider abstraction
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

# 🤖 Run with OpenAI-compatible LLM

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4o-mini"
uvicorn app.main:app --reload
```

---

# 🦙 Run with Ollama

```bash
ollama run llama3.1
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.1
uvicorn app.main:app --reload
```

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
docker build -t multi-agent-orchestrator:day4 .
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

Current test coverage includes:

- API behavior
- orchestration and retry logic
- event history persistence
- observability endpoints
- LLM-powered agent behavior with mock provider

---

# 📸 Diagrams and LinkedIn Assets

- `docs/architecture.md`
- `docs/sequence.md`
- `docs/day3-observability.md`
- `docs/sequence-day3.md`
- `docs/day4-llm-agents.md`
- `docs/sequence-day4.md`
- `docs/linkedin-post-day1.md`
- `docs/linkedin-post-day2.md`
- `docs/linkedin-post-day3.md`
- `docs/linkedin-post-day4.md`

---

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

# 📈 Future Improvements

- Helm chart
- OpenTelemetry tracing
- Redis or Kafka-backed event bus
- persistent storage
- CI/CD deployment pipeline
- real tool execution layer
- authentication and authorization

---

# 💡 Why this project

This project demonstrates how AI agents can be treated as platform workloads:

- orchestrated
- event-driven
- LLM-powered
- observable
- deployable
- testable

The goal is to move from AI demos to real AI Platform Engineering.
