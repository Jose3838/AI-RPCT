from intelligence.forecast.forecast_accuracy_engine_v4 import (
    forecast_accuracy_engine_v4
)

from intelligence.forecast.forecast_outcome_tracker import (
    forecast_outcome_tracker
)

def forecast_backtest_summary():

    accuracy = forecast_accuracy_engine_v4()
    outcome = forecast_outcome_tracker()

    return {
        "accuracy": accuracy,
        "outcome": outcome,
        "summary": (
            f"Forecast system has {accuracy.get('forecast_snapshots', 0)} historical snapshots "
            f"and an initial accuracy readiness score of {accuracy.get('accuracy_score', 0)}."
        )
    }
