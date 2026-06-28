from __future__ import annotations

from copilot.io import load_csv


def get_forecast_intelligence() -> dict:
    rows = load_csv("data/forecast_engine_v1_output.csv")

    if not rows:
        return {
            "status": "no forecast intelligence available"
        }

    return {
        "summary": {
            "status": "forecast intelligence available",
            "forecast_count": len(rows),
        },
        "metrics": {},
        "trends": {},
        "insights": [],
    }
