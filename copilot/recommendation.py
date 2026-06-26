from __future__ import annotations

from copilot.decision import get_decision


def priority_from_score(score: int) -> str:
    if score >= 80:
        return "high"

    if score >= 60:
        return "medium"

    return "low"


def get_recommendation() -> dict:
    decision = get_decision()

    if decision.get("status"):
        return decision

    try:
        confidence = float(decision["confidence"])
    except (KeyError, ValueError, TypeError):
        confidence = 0.0

    score = round(confidence * 100)
    priority = priority_from_score(score)

    return {
        "decision": decision["decision"],
        "confidence": confidence,
        "recommendation_score": score,
        "priority": priority,
        "topic": decision["topic"],
        "generated_at": decision["generated_at"],
    }
