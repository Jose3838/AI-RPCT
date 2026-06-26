from __future__ import annotations

from copilot.io import load_csv


def get_decision() -> dict:
    decisions = load_csv("data/decision_summary.csv")

    if not decisions:
        return {
            "status": "no decision available"
        }

    latest = decisions[0]

    return {
        "decision": latest.get("recommendation", ""),
        "confidence": latest.get("confidence", ""),
        "topic": latest.get("topic", ""),
        "generated_at": latest.get("generated_at", ""),
    }
