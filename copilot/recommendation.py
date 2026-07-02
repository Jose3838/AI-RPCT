from __future__ import annotations

from copilot.decision import get_decision
from copilot.intelligence.engine import get_unified_intelligence


def priority_from_score(score: int) -> str:
    if score >= 80:
        return "high"

    if score >= 60:
        return "medium"

    return "low"


def priority_reason_from_score(score: int) -> str:
    if score >= 80:
        return "Confidence is above 80%, indicating a strong recommendation."

    if score >= 60:
        return "Confidence is between 60% and 79%, indicating a moderate recommendation."

    return "Confidence is below 60%, indicating a low-confidence recommendation."


def get_recommendation() -> dict:
    decision = get_decision()
    intelligence = get_unified_intelligence()

    if decision.get("status"):
        return decision

    try:
        confidence = float(decision["confidence"])
    except (KeyError, ValueError, TypeError):
        confidence = 0.0

    score = round(confidence * 100)

    priority = priority_from_score(score)
    priority_reason = priority_reason_from_score(score)

    return {
        "decision": decision["decision"],
        "confidence": confidence,
        "recommendation_score": score,
        "priority": priority,
        "priority_reason": priority_reason,
        "topic": decision["topic"],
        "generated_at": decision["generated_at"],

        # Foundation for Recommendation Engine v2
        "intelligence": {
            "historical": intelligence["historical"]["summary"],
            "forecast": intelligence["forecast"].get("summary", {}),
            "capacity": intelligence["capacity"].get("summary", {}),
            "risk": intelligence["risk"].get("summary", {}),
            "pricing": intelligence["pricing"].get("summary", {}),
            "market": intelligence["market"].get("summary", {}),
        },
    }
