from __future__ import annotations

from copilot.io import load_csv


def get_risk_intelligence() -> dict:
    providers = load_csv("data/provider_entity_registry.csv")
    capacity = load_csv("data/historical_capacity_registry.csv")
    forecasts = load_csv("data/forecast_engine_v1_output.csv")

    provider_count = len(providers)
    capacity_records = len(capacity)
    forecast_records = len(forecasts)

    provider_risk = "low" if provider_count >= 5 else "high"
    capacity_risk = "low" if capacity_records >= 5 else "high"

    risk_score = 100

    if provider_risk == "high":
        risk_score -= 25

    if capacity_risk == "high":
        risk_score -= 20

    if forecast_records < 5:
        risk_score -= 20

    risk_score = max(0, risk_score)

    if risk_score >= 80:
        risk_severity = "low"
    elif risk_score >= 60:
        risk_severity = "medium"
    elif risk_score >= 40:
        risk_severity = "high"
    else:
        risk_severity = "critical"

    insight = (
        f"Current executive risk score: {risk_score}/100 "
        f"({risk_severity} risk)."
    )

    return {
        "summary": {
            "status": "risk intelligence available",
            "risk_score": risk_score,
            "risk_severity": risk_severity,
        },
        "metrics": {
            "provider_count": provider_count,
            "capacity_records": capacity_records,
            "forecast_records": forecast_records,
            "provider_risk": provider_risk,
            "capacity_risk": capacity_risk,
        },
        "trends": {},
        "insights": [
            {
                "type": "risk",
                "severity": risk_severity,
                "message": insight,
            }
        ],
    }
