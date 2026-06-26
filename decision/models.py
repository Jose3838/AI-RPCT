from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DecisionRecommendation:
    decision_id: str
    topic: str
    recommendation: str
    confidence: float
    evidence: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    rationale: str = ""
    generated_at: str = ""
