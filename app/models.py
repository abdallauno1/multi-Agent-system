from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    goal: str = Field(..., min_length=5, description="High-level task for the orchestrator")
    context: Dict[str, Any] = Field(default_factory=dict)


class Plan(BaseModel):
    steps: List[str]


class ExecutionResult(BaseModel):
    summary: str
    next_action: str
    confidence: float = Field(ge=0.0, le=1.0)
    details: Dict[str, Any] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    passed: bool
    reason: str


class RunRecord(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    goal: str
    context: Dict[str, Any] = Field(default_factory=dict)
    plan: List[str] = Field(default_factory=list)
    attempts: int = 0
    status: str = "created"
    result: Optional[ExecutionResult] = None
    validation: Optional[ValidationResult] = None
