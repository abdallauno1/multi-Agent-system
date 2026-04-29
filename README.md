# 🚀 Multi-Agent Orchestrator System

A production-style multi-agent system evolving from a simple orchestration model (Day 1) to an event-driven architecture (Day 2).

---

## 🧠 Project Vision

This project explores how to design and build **AI agent systems** using principles from:

- Platform Engineering
- Distributed Systems
- Event-Driven Architecture
- Observability-ready design

---

# 🥇 Day 1 — Core Multi-Agent System

## 🔧 What was built

- Planner Agent → creates execution plan  
- Executor Agent → executes tasks  
- Validator Agent → validates results  
- Orchestrator → manages workflow  
- Retry loop based on validation  
- Shared memory (basic persistence)  
- FastAPI interface  

## 🧩 Architecture

```
Client → FastAPI → Orchestrator
        → Planner → Executor → Validator
        → Retry (if failed)
        → Persist result
```

## 🎯 Key Concepts

- Agent orchestration  
- Task chaining  
- Validation-driven retry  
- Basic system coordination  

---

# 🥈 Day 2 — Event-Driven Architecture

## ⚡ What changed

The system evolved from synchronous calls to an **event-driven model**.

## 🔥 New Features

- Event Bus implementation  
- Decoupled agents  
- Event-based communication  
- Improved retry mechanism (event-driven)  
- Execution history (events tracking)  
- Enhanced shared memory  
- New API endpoints  

## 🧠 Event Flow

```
Orchestrator → Event Bus → Agents
```

Events:

- PLAN_CREATED  
- TASK_EXECUTE  
- TASK_COMPLETED  
- VALIDATION_REQUEST  
- VALIDATION_PASSED  
- VALIDATION_FAILED  
- RUN_COMPLETED  

## 🧩 Architecture (Day 2)

```
Client → FastAPI → Orchestrator
            ↓
        Event Bus
   ↙        ↓        ↘
Planner   Executor   Validator
            ↓
        Shared Memory
```

## 🎯 Key Improvements

- Decoupled system design  
- More scalable architecture  
- Closer to real distributed systems  
- Event-driven retry logic  

---

# 🛠️ Tech Stack

- Python  
- FastAPI  
- Event-driven architecture (custom EventBus)  
- JSON-based persistence  

---

# ▶️ How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# 📸 Diagrams

- docs/architecture.md  
- docs/sequence.md  

---

# 🧪 Example Request

```json
POST /runs
{
  "goal": "analyze logs"
}
```

---

# 📈 Roadmap

## 🔜 Day 3 (next)

- Kubernetes deployment  
- Observability (Prometheus + Grafana)  
- Logging & tracing  
- Production-ready improvements  

---

# 💡 Why this project

This is not a simple AI demo.

The goal is to build a **realistic AI platform system**, combining:

- AI Agents  
- Platform Engineering  
- Distributed Systems  

---

# ⭐ Author

Built as part of a hands-on journey into AI Platform Engineering.
