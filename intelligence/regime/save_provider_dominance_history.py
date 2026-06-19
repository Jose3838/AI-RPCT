import csv
from datetime import datetime, timezone
from pathlib import Path

from intelligence.regime.provider_dominance_regime import (
    provider_dominance_regime
)

FILE = Path("data/provider_dominance_regime_history.csv")


def save_provider_dominance_history():

    regime = provider_dominance_regime()

    FILE.parent.mkdir(parents=True, exist_ok=True)

    exists = FILE.exists()

    with FILE.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "status",
                "dominant_provider",
                "market_share_pct",
                "regime",
                "trend",
                "delta_pct",
                "hours_observed",
                "provider_count",
                "source_timestamp"
            ])

        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            regime.get("status"),
            regime.get("dominant_provider"),
            regime.get("market_share_pct"),
            regime.get("regime"),
            regime.get("trend"),
            regime.get("delta_pct"),
            regime.get("hours_observed"),
            regime.get("provider_count"),
            regime.get("latest_timestamp")
        ])

    return {
        "status": "saved",
        "file": str(FILE),
        "regime": regime
    }
