from __future__ import annotations

from copilot.io import load_csv


def get_risk_intelligence() -> dict:
    providers = load_csv("data/provider_entity_registry.csv")
    capacity = load_csv("data/historical_capacity_registry.csv")
    forecasts = load_csv("data/forecast_engine_v1_output.csv")

    provider_count = len(providers)
    capacity_records = len(capacity)
    forecast_records = len(forecasts)

    return {
        "summary": {
            "status": "risk intelligence available",
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
                "message": (
                    "Risk intelligence initialized. "
                    "Executive risk scoring will build on provider, "
                    "capacity and forecast datasets."
                ),
            }
        ],
    }
