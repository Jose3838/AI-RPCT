from forecast_history import load_forecast_history


def build_forecast_accuracy():
    history = load_forecast_history()

    if len(history) < 2:
        return {
            "status": "insufficient_history"
        }

    total_forecasts = len(history)

    matching_signals = 0

    previous_signal = None

    for row in history:

        current_signal = row["forecast_signal"]

        if previous_signal is not None:

            if current_signal == previous_signal:
                matching_signals += 1

        previous_signal = current_signal

    accuracy = round(
        (
            matching_signals
            /
            max(total_forecasts - 1, 1)
        )
        * 100,
        2
    )

    if accuracy >= 80:
        rating = "high_confidence"

    elif accuracy >= 60:
        rating = "moderate_confidence"

    else:
        rating = "low_confidence"

    return {
        "status": "ok",
        "version": "v1",
        "forecast_accuracy": accuracy,
        "confidence_rating": rating,
        "forecast_records": total_forecasts
    }
