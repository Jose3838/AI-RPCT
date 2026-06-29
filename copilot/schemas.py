from __future__ import annotations

from typing import TypedDict


class ExecutiveSnapshot(TypedDict):
    snapshot_id: str
    generated_at: str
    risk_score: int
    risk_severity: str
    recommendation: str
    source: str


class ExecutiveSummary(TypedDict):
    status: str
    generated_at: str
    overall_risk_score: int
    overall_risk_severity: str
    overall_recommendation: str
