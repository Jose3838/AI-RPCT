import csv
import os
from datetime import datetime, timezone

from intelligence.forecast.forecast_engine_v4 import (
    forecast_engine_v4
)

FILE = "data/forecast_audit_history.csv"

def save_forecast_audit():

    forecasts = forecast_engine_v4()

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not exists:

            writer.writerow([
                "timestamp",
                "gpu_model",
                "signal",
                "recent_price",
                "historical_price"
            ])

        for row in forecasts:

            writer.writerow([
                datetime.now(
                    timezone.utc
                ).isoformat(),
                row["gpu_model"],
                row["signal"],
                row["recent_price"],
                row["historical_price"]
            ])

    return {
        "saved": len(forecasts)
    }
