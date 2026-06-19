import csv
import os
from datetime import datetime, timezone

from intelligence.coverage.live_coverage_tracker import live_coverage_tracker

FILE = "data/live_coverage_history.csv"

def save_live_coverage_history():
    coverage = live_coverage_tracker()
    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "coverage_percent",
                "live_providers",
                "total_providers"
            ])

        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            coverage["coverage_percent"],
            coverage["live_providers"],
            coverage["total_providers"]
        ])

    return coverage
