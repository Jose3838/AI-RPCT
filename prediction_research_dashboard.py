from forecast_accuracy_v2 import (
    build_forecast_accuracy_v2
)
from forecast_engine_v3 import (
    build_forecast_engine_v3
)


def build_prediction_research_dashboard():

    accuracy = build_forecast_accuracy_v2()
    forecast = build_forecast_engine_v3()

    direction_accuracy = accuracy.get(
        "direction_accuracy",
        0
    )

    if direction_accuracy >= 80:
        model_status = "production_grade"

    elif direction_accuracy >= 60:
        model_status = "promising"

    else:
        model_status = "research_required"

    return {
        "status": "ok",
        "version": "v1",
        "direction_accuracy":
            direction_accuracy,
        "model_status":
            model_status,
        "current_forecast":
            forecast,
        "next_priority":
            "improve_prediction_accuracy"
    }
