# Architecture Diagram - Day 1


## High-Level Flow

```mermaid
flowchart TD
    A[Client / API Request] --> B[FastAPI Service]
    B --> C[Orchestrator]
    C --> D[Planner Agent]
    D --> E[Execution Plan]
    E --> F[Executor Agent]
    F --> G[Execution Result]
    G --> H[Validator Agent]
    H --> I{Passed?}
    I -- Yes --> J[Persist to Shared Memory]
    I -- No --> K[Retry Loop]
    K --> F
    J --> L[API Response]
```

## Agent Responsibilities

```mermaid
flowchart LR
    P[Planner Agent] -->|Creates steps| O[Orchestrator]
    E[Executor Agent] -->|Executes task| O
    V[Validator Agent] -->|Approves / rejects| O
    O --> M[Shared Memory]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI
    participant ORC as Orchestrator
    participant P as Planner
    participant E as Executor
    participant V as Validator
    participant MEM as Shared Memory

    U->>API: POST /runs
    API->>ORC: run(goal, context)
    ORC->>P: create plan
    P-->>ORC: steps

    loop retry until validation passes
        ORC->>E: execute(plan, context)
        E-->>ORC: result
        ORC->>V: validate(result)
        V-->>ORC: pass/fail
    end

    ORC->>MEM: persist run record
    ORC-->>API: completed run
    API-->>U: JSON response
```

## Day 1 Architectural Notes

- Planner, Executor, and Validator are separated to show clear role-based agents.
- Shared memory is intentionally simple now, but can evolve to Redis, Postgres, or a vector store.
- Retry loop is in the orchestrator to centralize control logic.
- FastAPI gives an API-first interface and makes the project demo-friendly.

## Day 2 Evolution

- add async execution
- add queue or event bus
- add structured logging
- add metrics endpoint

## Day 3 Evolution

- add Docker Compose and Kubernetes manifests
- add Prometheus / Grafana
- add deployment workflow

