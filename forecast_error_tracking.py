from forecast_accuracy_v2 import build_forecast_accuracy_v2


def build_forecast_error_tracking():
    accuracy = build_forecast_accuracy_v2()

    if accuracy.get("status") != "ok":
        return {
            "status": "insufficient_history"
        }

    comparisons = accuracy["comparisons"]

    errors = [
        item
        for item in comparisons
        if item["correct"] is False
    ]

    error_rate = round(
        (len(errors) / len(comparisons)) * 100,
        2
    ) if comparisons else 0

    return {
        "status": "ok",
        "version": "v1",
        "total_predictions": len(comparisons),
        "errors": len(errors),
        "error_rate": error_rate,
        "error_examples": errors
    }
