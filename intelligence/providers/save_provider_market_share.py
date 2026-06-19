import csv
import os
from datetime import datetime, timezone

from intelligence.signals.provider_supply_share import (
    provider_supply_share
)

FILE = "data/provider_market_share_history.csv"


def save_provider_market_share():

    shares = provider_supply_share()

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "provider",
                "share"
            ])

        ts = datetime.now(
            timezone.utc
        ).isoformat()

        for row in shares:

            writer.writerow([
                ts,
                row["provider"],
                row["share"]
            ])

    return {
        "saved": len(shares)
    }
