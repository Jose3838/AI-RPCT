from __future__ import annotations

from copilot.decision import get_decision


def get_recommendation() -> dict:
    decision = get_decision()

    if decision.get("status"):
        return decision

    try:
        confidence = float(decision["confidence"])
    except (KeyError, ValueError, TypeError):
        confidence = 0.0

    score = round(confidence * 100)

    return {
        "decision": decision["decision"],
        "confidence": confidence,
        "recommendation_score": score,
        "topic": decision["topic"],
        "generated_at": decision["generated_at"],
    }
