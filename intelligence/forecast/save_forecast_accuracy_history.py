import csv
from datetime import datetime, timezone
from pathlib import Path

from intelligence.forecast.forecast_accuracy_v2 import forecast_accuracy_v2

FILE = Path("data/forecast_accuracy_history.csv")


def save_forecast_accuracy_history():
    accuracy = forecast_accuracy_v2()

    FILE.parent.mkdir(parents=True, exist_ok=True)

    exists = FILE.exists()

    with FILE.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "status",
                "accuracy_score",
                "forecast_rows",
                "correct_rows",
                "signal_counts"
            ])

        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            accuracy.get("status"),
            accuracy.get("accuracy_score"),
            accuracy.get("forecast_rows"),
            accuracy.get("correct_rows"),
            accuracy.get("signal_counts")
        ])

    return {
        "status": "saved",
        "file": str(FILE),
        "accuracy": accuracy
    }
