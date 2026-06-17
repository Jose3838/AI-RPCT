from trend_intelligence import build_trend_intelligence
from gpu_scarcity_index import build_gpu_scarcity_index
from capacity_pressure_index import build_capacity_pressure_index
from infrastructure_risk_signal import build_infrastructure_risk_signal
from data_trust_index import build_data_trust_index


def build_forecast_engine_v3():

    trend = build_trend_intelligence()
    scarcity = build_gpu_scarcity_index()
    pressure = build_capacity_pressure_index()
    risk = build_infrastructure_risk_signal()
    trust = build_data_trust_index()

    score = 0

    if trend.get("trend_direction") == "up":
        score += 25

    if scarcity["gpu_scarcity_index"] >= 60:
        score += 20

    if pressure["capacity_pressure_index"] >= 65:
        score += 20

    if risk["risk_level"] in ["high", "critical"]:
        score += 20

    if trust["data_trust_index"] >= 80:
        score += 15

    if score >= 80:
        signal = "strong_capacity_shortage_expected"
    elif score >= 60:
        signal = "capacity_tightening_expected"
    elif score >= 40:
        signal = "balanced_market_expected"
    else:
        signal = "stable_market_expected"

    return {
        "status": "ok",
        "version": "v3",
        "forecast_score": score,
        "forecast_signal": signal,
        "trend_direction": trend.get("trend_direction", "unknown"),
        "risk_level": risk["risk_level"],
        "data_trust": trust["trust_status"]
    }
