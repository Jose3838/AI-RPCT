from forecast_engine_v3 import build_forecast_engine_v3
from forecast_weight_optimization import build_forecast_weight_optimization


def build_forecast_engine_v31():
    forecast = build_forecast_engine_v3()
    optimization = build_forecast_weight_optimization()

    adjusted_score = forecast["forecast_score"]

    if optimization["weighting_strategy"] == "increase_signal_sensitivity":
        adjusted_score = min(adjusted_score + 10, 100)

    elif optimization["weighting_strategy"] == "reduce_signal_sensitivity":
        adjusted_score = max(adjusted_score - 10, 0)

    elif optimization["weighting_strategy"] == "research_mode":
        adjusted_score = max(adjusted_score - 20, 0)

    return {
        "status": "ok",
        "version": "v3.1",
        "base_forecast": forecast,
        "optimization": optimization,
        "adjusted_forecast_score": adjusted_score
    }
