from infrastructure_risk_signal import build_infrastructure_risk_signal
from forecast_engine_v2 import build_forecast_engine_v2
from gpu_scarcity_index import build_gpu_scarcity_index
from capacity_pressure_index import build_capacity_pressure_index
from data_trust_index import build_data_trust_index


def build_executive_market_briefing():

    risk = build_infrastructure_risk_signal()
    forecast = build_forecast_engine_v2()
    scarcity = build_gpu_scarcity_index()
    pressure = build_capacity_pressure_index()
    trust = build_data_trust_index()

    return {
        "status": "ok",
        "version": "v1",
        "briefing_type": "executive_market_briefing",
        "market_forecast": forecast,
        "gpu_scarcity": scarcity,
        "capacity_pressure": pressure,
        "infrastructure_risk": risk,
        "data_trust": trust,
        "executive_summary": {
            "market_signal": forecast.get(
                "forecast_signal",
                "unknown"
            ),
            "risk_level": risk["risk_level"],
            "trust_status": trust["trust_status"]
        }
    }
