from forecast_error_tracking import build_forecast_error_tracking
from forecast_accuracy_v2 import build_forecast_accuracy_v2


def build_forecast_model_improvement_plan():
    errors = build_forecast_error_tracking()
    accuracy = build_forecast_accuracy_v2()

    direction_accuracy = accuracy.get(
        "direction_accuracy",
        0
    )

    error_rate = errors.get(
        "error_rate",
        100
    )

    if direction_accuracy >= 80:
        priority = "optimize_model"
        recommendation = "Continue collecting data and tune thresholds."

    elif direction_accuracy >= 60:
        priority = "improve_signal_weighting"
        recommendation = "Rebalance trend, scarcity, pressure, and risk weights."

    else:
        priority = "research_required"
        recommendation = "Collect more snapshots and reduce reliance on single-day noise."

    return {
        "status": "ok",
        "version": "v1",
        "direction_accuracy": direction_accuracy,
        "error_rate": error_rate,
        "priority": priority,
        "recommendation": recommendation
    }
