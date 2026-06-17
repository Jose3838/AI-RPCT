from capacity_pressure_index import build_capacity_pressure_index
from forecast_engine_v2 import build_forecast_engine_v2
from data_trust_index import build_data_trust_index


def build_infrastructure_risk_signal():
    pressure = build_capacity_pressure_index()
    forecast = build_forecast_engine_v2()
    trust = build_data_trust_index()

    pressure_score = pressure["capacity_pressure_index"]
    trust_score = trust["data_trust_index"]

    if pressure_score >= 80:
        risk_level = "critical"
    elif pressure_score >= 65:
        risk_level = "high"
    elif pressure_score >= 50:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "status": "ok",
        "version": "v1",
        "risk_level": risk_level,
        "capacity_pressure_index": pressure_score,
        "forecast_signal": forecast.get("forecast_signal", "unknown"),
        "forecast_confidence": forecast.get("confidence", "unknown"),
        "data_trust_index": trust_score,
        "enterprise_action": (
            "Secure GPU capacity early and monitor provider availability."
            if risk_level in ["critical", "high"]
            else "Continue monitoring market conditions."
        )
    }
