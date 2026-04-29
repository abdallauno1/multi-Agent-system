from __future__ import annotations

from typing import Callable, Dict, List

from app.models import RunEvent


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[RunEvent], None]]] = {}
        self._events: List[RunEvent] = []

    def subscribe(self, event_type: str, handler: Callable[[RunEvent], None]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: dict, run_id: str, source: str) -> RunEvent:
        event = RunEvent(
            event_type=event_type,
            run_id=run_id,
            source=source,
            payload=payload,
        )
        self._events.append(event)

        for handler in self._subscribers.get(event_type, []):
            handler(event)

        return event

    def snapshot(self) -> List[RunEvent]:
        return list(self._events)

    def reset(self) -> None:
        self._events = []