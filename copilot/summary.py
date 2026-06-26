from __future__ import annotations

from copilot.io import load_csv


def get_summary() -> dict:
    rows = load_csv("data/executive_morning_brief.csv")

    if not rows:
        return {
            "status": "no executive summary available"
        }

    return rows[0]
