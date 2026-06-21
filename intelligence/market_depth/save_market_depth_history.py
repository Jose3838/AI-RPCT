import csv
import os
from datetime import datetime, timezone

from intelligence.market_depth.gpu_market_depth import (
    gpu_market_depth
)

FILE = (
    "data/feature_store/"
    "gpu_market_depth_history.csv"
)

def save_market_depth_history():

    rows = gpu_market_depth()

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "gpu_model",
                "offer_count",
                "avg_price",
                "min_price",
                "max_price"
            ])

        ts = datetime.now(
            timezone.utc
        ).isoformat()

        for row in rows:

            writer.writerow([
                ts,
                row["gpu_model"],
                row["offer_count"],
                row["avg_price"],
                row["min_price"],
                row["max_price"]
            ])

    return {
        "saved": len(rows)
    }
