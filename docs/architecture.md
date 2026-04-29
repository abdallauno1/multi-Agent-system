# Architecture Diagram - Day 2


## Event-Driven Architecture

```mermaid
flowchart LR
    U[Client / API Request] --> API[FastAPI Service]
    API --> O[Orchestrator]
    O --> B[Event Bus]
    B --> P[Planner Agent]
    B --> E[Executor Agent]
    B --> V[Validator Agent]
    O --> M[Shared Memory]
    M --> R[Run History + Event Log]
```

## Agent Responsibility View

```mermaid
flowchart LR
    P[Planner Agent] -->|creates plan events| B[Event Bus]
    E[Executor Agent] -->|emits execution results| B
    V[Validator Agent] -->|approves or rejects| B
    B --> O[Orchestrator]
    O --> M[Shared Memory]
```

## Day 2 Notes

- the event bus decouples workflow transitions from direct method chaining
- each run now stores an event history for replay and debugging
- validation failure triggers a new execution event instead of a raw loop-only flow
- shared memory is still file-based now, but it can evolve to Redis or Postgres in Day 3
