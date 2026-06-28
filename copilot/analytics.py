from __future__ import annotations

from copilot.io import load_csv


def get_analytics() -> dict:
    rows = load_csv("data/decision_history.csv")

    if not rows:
        return {
            "status": "no analytics available"
        }

    confidences = []

    for row in rows:
        try:
            confidences.append(float(row["confidence"]))
        except (KeyError, ValueError, TypeError):
            continue

    if not confidences:
        return {
            "status": "no confidence values available"
        }

    return {
        "decision_count": len(rows),
        "average_confidence": round(sum(confidences) / len(confidences), 2),
        "max_confidence": max(confidences),
        "min_confidence": min(confidences),
    }
