from __future__ import annotations

from copilot.io import load_csv


def get_decision_intelligence() -> dict:
    rows = load_csv("data/decision_history.csv")

    if not rows:
        return {
            "status": "no decision intelligence available"
        }

    recommendations = {
        row.get("recommendation", "").strip()
        for row in rows
        if row.get("recommendation")
    }

    latest_decision = rows[-1]

    return {
        "summary": {
            "status": "decision intelligence available",
            "decision_count": len(rows),
            "latest_decision": latest_decision.get("generated_at"),
        },
        "metrics": {
            "recommendation_count": len(recommendations),
            "recommendation_consistency": len(recommendations) == 1,
        },
        "trends": {},
        "insights": [],
    }
