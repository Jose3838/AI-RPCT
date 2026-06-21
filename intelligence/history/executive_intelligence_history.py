import csv
import os
from datetime import datetime, timezone

from intelligence.executive.daily_executive_intelligence import (
    daily_executive_intelligence
)

FILE = "data/executive_intelligence_history.csv"

def save_executive_intelligence():

    intelligence = daily_executive_intelligence()

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "opportunity_count",
                "risk_count"
            ])

        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            len(intelligence["opportunities"]),
            len(intelligence["risks"])
        ])

    return intelligence
