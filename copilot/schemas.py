from __future__ import annotations

from typing import TypedDict


class ExecutiveSnapshot(TypedDict):
    snapshot_id: str
    generated_at: str
    risk_score: int
    risk_severity: str
    recommendation: str
    source: str
