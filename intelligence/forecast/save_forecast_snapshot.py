import csv
import os
from datetime import datetime, timezone

from intelligence.forecast.alpha_candidates import (
    alpha_candidates
)

FILE = "data/forecast_snapshot_history.csv"

def save_forecast_snapshot():

    forecasts = alpha_candidates()

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "alpha_candidates"
            ])

        writer.writerow([
            datetime.now(
                timezone.utc
            ).isoformat(),
            len(forecasts)
        ])

    return {
        "saved": len(forecasts)
    }
