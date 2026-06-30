from __future__ import annotations

from copilot.intelligence_hub import get_intelligence_hub


def get_executive_dashboard() -> dict:
    hub = get_intelligence_hub()

    risk_summary = hub.get("risk", {}).get("summary", {})
    executive_summary = hub.get("executive", {}).get("summary", {})
    forecast_summary = hub.get("forecast", {}).get("summary", {})
    provider_summary = hub.get("provider", {}).get("summary", {})
    capacity_summary = hub.get("capacity", {}).get("summary", {})
    pipeline_health = hub.get("pipeline", {}).get("health", {})

    return {
        "status": "executive dashboard available",
        "kpis": {
            "pipeline_health": pipeline_health.get("pipeline_health"),
            "pipeline_status": pipeline_health.get("status"),
            "pipeline_success_rate": pipeline_health.get("success_rate"),
            "risk_score": risk_summary.get(
                "risk_score",
                executive_summary.get("overall_risk_score"),
            ),
            "risk_severity": risk_summary.get(
                "risk_severity",
                executive_summary.get("overall_risk_severity"),
            ),
            "recommendation": risk_summary.get(
                "recommendation",
                executive_summary.get("overall_recommendation"),
            ),
            "forecast_status": forecast_summary.get("status"),
            "provider_count": provider_summary.get("provider_count"),
            "active_provider_count": provider_summary.get(
                "active_provider_count"
            ),
            "capacity_records": capacity_summary.get("capacity_records"),
        },
        "sections": {
            "executive": executive_summary,
            "risk": risk_summary,
            "forecast": forecast_summary,
            "provider": provider_summary,
            "capacity": capacity_summary,
            "pipeline": pipeline_health,
        },
    }
