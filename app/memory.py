from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.models import RunRecord


class RunMemory:
    def __init__(self, path: str = "runs.json") -> None:
        self.path = Path(path)
        self.records: List[RunRecord] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        raw = json.loads(self.path.read_text())
        self.records = [RunRecord(**item) for item in raw]

    def _save(self) -> None:
        self.path.write_text(
            json.dumps([record.model_dump() for record in self.records], indent=2)
        )

    def add(self, record: RunRecord) -> None:
        self.records.append(record)
        self._save()

    def all(self) -> List[RunRecord]:
        return self.records
