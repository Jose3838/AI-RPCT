from intelligence.forecast.forecast_accuracy_engine_v4 import (
    forecast_accuracy_engine_v4
)

from intelligence.forecast.forecast_outcome_tracker import (
    forecast_outcome_tracker
)

from intelligence.forecast.forecast_accuracy_v2 import (
    forecast_accuracy_v2
)

from intelligence.forecast.forecast_backtesting_v2 import (
    forecast_backtesting_v2
)


def forecast_backtest_summary():

    accuracy = forecast_accuracy_engine_v4()
    outcome = forecast_outcome_tracker()
    accuracy_v2 = forecast_accuracy_v2()
    backtesting_v2 = forecast_backtesting_v2()

    return {
        "accuracy": accuracy,
        "accuracy_v2": accuracy_v2,
        "backtesting_v2": backtesting_v2,
        "outcome": outcome,
        "summary": (
            f"Forecast Accuracy V2 is {accuracy_v2.get('accuracy_score', 0)}. "
            f"Backtest readiness is {backtesting_v2.get('backtest_readiness_score', 0)}."
        )
    }
