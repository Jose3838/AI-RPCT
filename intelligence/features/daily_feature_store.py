import os
import csv
from datetime import datetime, timezone

from intelligence.signals.market_supply_index import (
    calculate_market_supply_index
)

from intelligence.signals.gpu_price_index import (
    calculate_gpu_price_index
)

FEATURE_FILE = (
    "data/feature_store/"
    "daily_market_features.csv"
)

FIELDS = [
    "timestamp",
    "gpu_price_index",
    "market_supply_index"
]

def append_daily_features():

    supply = calculate_market_supply_index()
    price = calculate_gpu_price_index()

    row = {
        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "gpu_price_index":
            price["gpu_price_index"]
            if price else None,

        "market_supply_index":
            supply["supply_index"]
            if supply else None,
    }

    exists = os.path.exists(
        FEATURE_FILE
    )

    with open(
        FEATURE_FILE,
        "a",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=FIELDS
        )

        if not exists:
            writer.writeheader()

        writer.writerow(row)

    return row
