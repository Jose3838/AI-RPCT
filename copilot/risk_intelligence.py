from __future__ import annotations

from copilot.io import load_csv


def get_risk_intelligence() -> dict:
    providers = load_csv("data/provider_entity_registry.csv")
    capacity = load_csv("data/historical_capacity_registry.csv")
    forecasts = load_csv("data/forecast_engine_v1_output.csv")

    provider_count = len(providers)
    capacity_records = len(capacity)
    forecast_records = len(forecasts)

    risk_score = 100

    if provider_count < 5:
        risk_score -= 25

    if capacity_records < 5:
        risk_score -= 20

    if forecast_records < 5:
        risk_score -= 20

    risk_score = max(0, risk_score)

    insight = (
        f"Current executive risk score: {risk_score}/100."
    )

    return {
        "summary": {
            "status": "risk intelligence available",
            "risk_score": risk_score,
        },
        "metrics": {
            "provider_count": provider_count,
            "capacity_records": capacity_records,
            "forecast_records": forecast_records,
        },
        "trends": {},
        "insights": [
            {
                "type": "risk",
                "severity": "info",
                "message": insight,
            }
        ],
    }
