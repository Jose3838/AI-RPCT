from forecast_validation_store import (
    load_forecasts,
    load_market_history
)


def infer_expected_direction(forecast_signal):
    if forecast_signal in [
        "strong_capacity_shortage_expected",
        "capacity_tightening_expected",
        "moderate_growth_expected",
        "strong_growth_expected"
    ]:
        return "up"

    if forecast_signal in [
        "market_weakness_expected",
        "slight_weakness_expected"
    ]:
        return "down"

    return "flat"


def infer_actual_direction(previous_strength, current_strength):
    change = current_strength - previous_strength

    if change > 0:
        return "up"

    if change < 0:
        return "down"

    return "flat"


def get_forecast_time(row):
    return row.get("timestamp") or row.get("date") or "unknown"


def build_forecast_accuracy_v2():
    forecasts = load_forecasts()
    market = load_market_history()

    if len(forecasts) < 2 or len(market) < 2:
        return {
            "status": "insufficient_history",
            "forecast_records": len(forecasts),
            "market_records": len(market)
        }

    comparisons = []
    correct = 0

    limit = min(len(forecasts), len(market)) - 1

    for index in range(limit):
        forecast = forecasts[index]
        previous_market = market[index]
        current_market = market[index + 1]

        expected_direction = infer_expected_direction(
            forecast["forecast_signal"]
        )

        actual_direction = infer_actual_direction(
            float(previous_market["market_strength"]),
            float(current_market["market_strength"])
        )

        is_correct = expected_direction == actual_direction

        if is_correct:
            correct += 1

        comparisons.append({
            "forecast_time": get_forecast_time(forecast),
            "expected_direction": expected_direction,
            "actual_direction": actual_direction,
            "correct": is_correct
        })

    accuracy = round(
        (correct / limit) * 100,
        2
    ) if limit else 0

    return {
        "status": "ok",
        "version": "v2",
        "direction_accuracy": accuracy,
        "comparisons": comparisons
    }
