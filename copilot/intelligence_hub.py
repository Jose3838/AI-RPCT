from __future__ import annotations

from copilot.capacity_intelligence import get_capacity_intelligence
from copilot.change_intelligence import get_change_intelligence
from copilot.decision_intelligence import get_decision_intelligence
from copilot.executive.intelligence import get_executive_intelligence
from copilot.forecast_intelligence import get_forecast_intelligence
from copilot.provider_intelligence import get_provider_intelligence
from copilot.risk_intelligence import get_risk_intelligence
from copilot.io import load_csv


def get_pipeline_health() -> dict:
    rows = load_csv("data/pipeline_intelligence.csv")

    if not rows:
        return {
            "status": "pipeline unavailable"
        }

    return rows[0]


def get_pipeline_history() -> list[dict]:
    return load_csv("data/pipeline_history.csv")


def get_intelligence_hub() -> dict:
    return {
        "status": "intelligence hub available",
        "executive": get_executive_intelligence(),
        "risk": get_risk_intelligence(),
        "forecast": get_forecast_intelligence(),
        "decision": get_decision_intelligence(),
        "provider": get_provider_intelligence(),
        "capacity": get_capacity_intelligence(),
        "change": get_change_intelligence(),
        "pipeline": {
            "health": get_pipeline_health(),
            "history": get_pipeline_history(),
        },
    }
