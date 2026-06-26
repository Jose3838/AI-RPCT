from __future__ import annotations

from copilot.decision import get_decision


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
    }
