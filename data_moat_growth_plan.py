from data_moat_dashboard import build_data_moat_dashboard
from intelligence_performance_dashboard import build_intelligence_performance_dashboard


def build_data_moat_growth_plan():
    moat = build_data_moat_dashboard()
    performance = build_intelligence_performance_dashboard()

    score = moat["data_moat_score"]

    if score < 20:
        priority = "increase_snapshot_frequency"
        recommendation = "Run intelligence snapshots hourly to accelerate historical data accumulation."
    elif score < 60:
        priority = "expand_historical_depth"
        recommendation = "Continue daily and hourly snapshots across all intelligence datasets."
    else:
        priority = "optimize_forecasting"
        recommendation = "Use accumulated history to improve model weights and forecast accuracy."

    return {
        "status": "ok",
        "version": "v1",
        "data_moat_score": score,
        "forecast_accuracy": performance["forecast_accuracy"],
        "priority": priority,
        "recommendation": recommendation
    }
