import csv
import os
from datetime import datetime, timezone

from intelligence.regime.market_regime_engine import (
    market_regime_engine
)

FILE = "data/regime_history.csv"

def save_market_regime_history():

    regime = market_regime_engine()

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "regime",
                "observations",
                "providers",
                "gpu_models"
            ])

        writer.writerow([
            datetime.now(
                timezone.utc
            ).isoformat(),
            regime["regime"],
            regime["observations"],
            regime["providers"],
            regime["gpu_models"]
        ])

    return regime
