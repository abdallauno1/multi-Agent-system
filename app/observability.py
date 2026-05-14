from __future__ import annotations

import json
import logging
import time
from contextlib import contextmanager
from typing import Any, Iterator

from prometheus_client import Counter, Gauge, Histogram


logger = logging.getLogger("multi_agent_orchestrator")
logging.basicConfig(level=logging.INFO, format="%(message)s")

RUNS_TOTAL = Counter(
    "multi_agent_runs_total",
    "Total number of multi-agent runs by final status.",
    ["status"],
)

EVENTS_TOTAL = Counter(
    "multi_agent_events_total",
    "Total number of internal orchestration events.",
    ["event_type", "source"],
)

AGENT_EXECUTION_SECONDS = Histogram(
    "multi_agent_agent_execution_seconds",
    "Agent execution latency in seconds.",
    ["agent"],
)

RUN_DURATION_SECONDS = Histogram(
    "multi_agent_run_duration_seconds",
    "End-to-end run duration in seconds.",
)

ACTIVE_RUNS = Gauge(
    "multi_agent_active_runs",
    "Number of currently active orchestrator runs.",
)


def log_event(message: str, **fields: Any) -> None:
    payload = {"message": message, **fields}
    logger.info(json.dumps(payload, default=str))


@contextmanager
def track_agent_latency(agent: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        AGENT_EXECUTION_SECONDS.labels(agent=agent).observe(time.perf_counter() - start)
