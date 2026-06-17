from provider_recommendation_engine import build_provider_recommendations
from infrastructure_risk_signal import build_infrastructure_risk_signal
from forecast_engine_v2 import build_forecast_engine_v2
from data_trust_index import build_data_trust_index


def build_enterprise_decision_engine():
    recommendations = build_provider_recommendations()
    risk = build_infrastructure_risk_signal()
    forecast = build_forecast_engine_v2()
    trust = build_data_trust_index()

    risk_level = risk["risk_level"]
    trust_score = trust["data_trust_index"]

    if risk_level in ["critical", "high"] and trust_score >= 75:
        decision = "buy_capacity_now"
    elif risk_level == "medium" and trust_score >= 75:
        decision = "secure_selective_capacity"
    elif trust_score < 60:
        decision = "wait_for_better_data"
    else:
        decision = "monitor_market"

    return {
        "status": "ok",
        "version": "v1",
        "decision": decision,
        "risk_level": risk_level,
        "forecast_signal": forecast.get("forecast_signal", "unknown"),
        "data_trust_index": trust_score,
        "provider_recommendations": recommendations["recommendations"]
    }
