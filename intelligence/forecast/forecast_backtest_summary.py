from intelligence.forecast.forecast_accuracy_engine_v4 import (
    forecast_accuracy_engine_v4
)

from intelligence.forecast.forecast_outcome_tracker import (
    forecast_outcome_tracker
)

from intelligence.forecast.forecast_accuracy_v2 import (
    forecast_accuracy_v2
)


def forecast_backtest_summary():

    accuracy = forecast_accuracy_engine_v4()
    outcome = forecast_outcome_tracker()
    accuracy_v2 = forecast_accuracy_v2()

    return {
        "accuracy": accuracy,
        "accuracy_v2": accuracy_v2,
        "outcome": outcome,
        "summary": (
            f"Forecast system has {accuracy.get('forecast_snapshots', 0)} historical snapshots "
            f"and Forecast Accuracy V2 score is {accuracy_v2.get('accuracy_score', 0)}."
        )
    }
