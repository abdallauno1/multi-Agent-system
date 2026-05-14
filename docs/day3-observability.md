# Day 3 — Kubernetes + Observability

Day 3 turns the event-driven multi-agent runtime into a production-style platform component.

## What was added

- Docker runtime
- Docker Compose local stack
- Prometheus metrics endpoint: `/metrics`
- Grafana dashboard provisioning
- Kubernetes manifests
- readiness and liveness probes
- structured JSON logs
- CI-friendly tests for observability endpoints

## Runtime Architecture

```mermaid
flowchart LR
    User[User / API Client] --> API[FastAPI Service]
    API --> Orch[Multi-Agent Orchestrator]
    Orch --> Bus[Event Bus]
    Bus --> Planner[Planner Agent]
    Bus --> Executor[Executor Agent]
    Bus --> Validator[Validator Agent]
    Orch --> Memory[Shared Memory]

    API --> Metrics[/Prometheus Metrics/]
    Prom[Prometheus] --> Metrics
    Grafana[Grafana Dashboard] --> Prom
```

## Kubernetes View

```mermaid
flowchart TB
    subgraph K8s[Kubernetes Cluster]
        NS[Namespace: multi-agent-system]
        Deploy[Deployment: multi-agent-orchestrator]
        Pods[2 API Pods]
        Svc[ClusterIP Service]
        HPA[HorizontalPodAutoscaler]
    end

    User[Client] --> Svc
    Svc --> Pods
    Deploy --> Pods
    HPA --> Deploy
    Pods --> Health[/health + /ready/]
    Pods --> Metrics[/metrics/]
    Prometheus[Prometheus] --> Metrics
```

## Metrics exposed

- `multi_agent_runs_total{status="completed|failed"}`
- `multi_agent_events_total{event_type="...", source="..."}`
- `multi_agent_agent_execution_seconds_bucket{agent="planner|executor|validator"}`
- `multi_agent_run_duration_seconds_bucket`
- `multi_agent_active_runs`

## Local observability stack

```bash
docker compose up --build
```

Open:

- API docs: `http://localhost:8000/docs`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

Grafana login:

- username: `admin`
- password: `admin`
