from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, List

from app.models import RunEvent

EventHandler = Callable[[RunEvent], None]


class EventBus:
    def __init__(self) -> None:
        self.subscribers: DefaultDict[str, List[EventHandler]] = defaultdict(list)
        self._events: List[RunEvent] = []

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self.subscribers[event_type].append(handler)

    def publish(
        self,
        event_type: str,
        payload: Dict[str, Any],
        *,
        run_id: str,
        source: str,
    ) -> RunEvent:
        event = RunEvent(event_type=event_type, payload=payload, run_id=run_id, source=source)
        self._events.append(event)
        for handler in self.subscribers[event_type]:
            handler(event)
        return event

    def snapshot(self) -> List[RunEvent]:
        return list(self._events)

    def reset(self) -> None:
        self._events.clear()
