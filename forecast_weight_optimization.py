from forecast_accuracy_v2 import build_forecast_accuracy_v2


def build_forecast_weight_optimization():
    accuracy = build_forecast_accuracy_v2()

    direction_accuracy = accuracy.get(
        "direction_accuracy",
        0
    )

    if direction_accuracy >= 80:
        weighting_strategy = "increase_signal_sensitivity"
        recommendation = "Model can trust current signals more aggressively."
    elif direction_accuracy >= 60:
        weighting_strategy = "maintain_current_weights"
        recommendation = "Model is acceptable but needs more data."
    elif direction_accuracy >= 40:
        weighting_strategy = "reduce_signal_sensitivity"
        recommendation = "Model should be more conservative."
    else:
        weighting_strategy = "research_mode"
        recommendation = "Do not increase forecast confidence until more history exists."

    return {
        "status": "ok",
        "version": "v1",
        "direction_accuracy": direction_accuracy,
        "weighting_strategy": weighting_strategy,
        "recommendation": recommendation
    }
