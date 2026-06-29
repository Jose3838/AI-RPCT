from __future__ import annotations

from copilot.analytics import get_analytics
from copilot.capacity_intelligence import get_capacity_intelligence
from copilot.decision_intelligence import get_decision_intelligence
from copilot.forecast_intelligence import get_forecast_intelligence
from copilot.provider_intelligence import get_provider_intelligence
from copilot.risk_intelligence import get_risk_intelligence
from copilot.summary import get_summary


def get_executive_intelligence() -> dict:
    summary = get_summary()
    analytics = get_analytics()
    decision = get_decision_intelligence()
    forecast = get_forecast_intelligence()
    provider = get_provider_intelligence()
    capacity = get_capacity_intelligence()
    risk = get_risk_intelligence()

    return {
        "summary": {
            "status": "executive intelligence available",
        },
        "modules": {
            "summary": summary,
            "analytics": analytics,
            "decision_intelligence": decision,
            "forecast_intelligence": forecast,
            "provider_intelligence": provider,
            "capacity_intelligence": capacity,
            "risk_intelligence": risk,
        },
    }
