from __future__ import annotations

from copilot.io import load_csv


def get_decision_timeline(limit: int = 10) -> dict:
    rows = load_csv("data/decision_history.csv")

    if not rows:
        return {
            "status": "no decision history available"
        }

    latest = rows[-limit:]

    return {
        "count": len(rows),
        "returned": len(latest),
        "timeline": latest,
    }
