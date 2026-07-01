from __future__ import annotations

from copilot.io import load_csv


def _risk_level_from_count(count: int, healthy_threshold: int) -> str:
    if count >= healthy_threshold:
        return "low"

    return "high"


def _risk_penalty(level: str, high_penalty: int, medium_penalty: int) -> int:
    if level == "high":
        return high_penalty

    return 0


def get_risk_intelligence() -> dict:
    providers = load_csv("data/provider_entity_registry.csv")
    capacity = load_csv("data/historical_capacity_registry.csv")
    forecasts = load_csv("data/forecast_engine_v1_output.csv")

    provider_count = len(providers)
    capacity_records = len(capacity)
    forecast_records = len(forecasts)

    provider_risk = _risk_level_from_count(
        provider_count,
        healthy_threshold=5,
    )
    capacity_risk = _risk_level_from_count(
        capacity_records,
        healthy_threshold=5,
    )
    forecast_risk = _risk_level_from_count(
        forecast_records,
        healthy_threshold=5,
    )

    provider_penalty = _risk_penalty(
        provider_risk,
        high_penalty=25,
        medium_penalty=10,
    )
    capacity_penalty = _risk_penalty(
        capacity_risk,
        high_penalty=20,
        medium_penalty=10,
    )
    forecast_penalty = _risk_penalty(
        forecast_risk,
        high_penalty=20,
        medium_penalty=10,
    )

    risk_score = max(
        0,
        100 - provider_penalty - capacity_penalty - forecast_penalty,
    )

    provider_risk_score = max(0, 100 - provider_penalty)
    capacity_risk_score = max(0, 100 - capacity_penalty)
    forecast_risk_score = max(0, 100 - forecast_penalty)

    if risk_score >= 80:
        risk_severity = "low"
        recommendation = "Continue monitoring current infrastructure."
    elif risk_score >= 60:
        risk_severity = "medium"
        recommendation = "Review infrastructure risks regularly."
    elif risk_score >= 40:
        risk_severity = "high"
        recommendation = "Investigate provider and capacity risks."
    else:
        risk_severity = "critical"
        recommendation = "Immediate executive review recommended."

    risk_drivers = []

    if provider_risk != "low":
        risk_drivers.append(
            {
                "area": "provider",
                "severity": provider_risk,
                "message": (
                    f"Provider coverage is {provider_risk} with "
                    f"{provider_count} provider records."
                ),
            }
        )

    if capacity_risk != "low":
        risk_drivers.append(
            {
                "area": "capacity",
                "severity": capacity_risk,
                "message": (
                    f"Capacity coverage is {capacity_risk} with "
                    f"{capacity_records} capacity records."
                ),
            }
        )

    if forecast_risk != "low":
        risk_drivers.append(
            {
                "area": "forecast",
                "severity": forecast_risk,
                "message": (
                    f"Forecast coverage is {forecast_risk} with "
                    f"{forecast_records} forecast records."
                ),
            }
        )

    if not risk_drivers:
        risk_drivers.append(
            {
                "area": "platform",
                "severity": "low",
                "message": (
                    "No elevated provider, capacity, or forecast risk "
                    "drivers detected."
                ),
            }
        )

    risk_explanation = (
        f"Risk score is {risk_score}/100. "
        f"Provider risk is {provider_risk}, capacity risk is "
        f"{capacity_risk}, and forecast risk is {forecast_risk}."
    )

    insight = (
        f"Current executive risk score: {risk_score}/100 "
        f"({risk_severity} risk)."
    )

    return {
        "summary": {
            "status": "risk intelligence available",
            "risk_score": risk_score,
            "risk_severity": risk_severity,
            "recommendation": recommendation,
            "risk_explanation": risk_explanation,
        },
        "metrics": {
            "provider_count": provider_count,
            "capacity_records": capacity_records,
            "forecast_records": forecast_records,
            "provider_risk": provider_risk,
            "capacity_risk": capacity_risk,
            "forecast_risk": forecast_risk,
            "provider_risk_score": provider_risk_score,
            "capacity_risk_score": capacity_risk_score,
            "forecast_risk_score": forecast_risk_score,
        },
        "trends": {},
        "risk_drivers": risk_drivers,
        "insights": [
            {
                "type": "risk",
                "severity": risk_severity,
                "message": insight,
            }
        ],
    }
