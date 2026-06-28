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

    return {
        "summary": {
            "status": "decision intelligence available",
            "decision_count": len(rows),
        },
        "metrics": {
            "recommendation_count": len(recommendations),
            "recommendation_consistency": len(recommendations) == 1,
        },
        "trends": {},
        "insights": [],
    }
