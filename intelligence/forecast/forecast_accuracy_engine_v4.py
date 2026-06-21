from intelligence.forecast.forecast_outcome_tracker import (
    forecast_outcome_tracker
)

def forecast_accuracy_engine_v4():

    outcome = forecast_outcome_tracker()

    if outcome.get("status") == "no_data":
        return {
            "status": "insufficient_data",
            "accuracy_score": 0
        }

    snapshots = outcome.get("snapshots", 0)

    score = min(
        100,
        snapshots * 5
    )

    return {
        "status": "ok",
        "forecast_snapshots": snapshots,
        "accuracy_score": score
    }
