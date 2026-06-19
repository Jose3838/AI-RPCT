import csv
from datetime import datetime, timezone
from pathlib import Path

from intelligence.signals.provider_supply_share import (
    provider_supply_share
)

FILE = Path("data/provider_market_share_history.csv")


def _normalize_share_row(row):
    provider = row.get("provider")

    rows = (
        row.get("rows")
        or row.get("offer_count")
        or row.get("observations")
        or row.get("count")
        or 0
    )

    market_share_pct = (
        row.get("market_share_pct")
        or row.get("share_pct")
        or row.get("share")
        or 0
    )

    return {
        "provider": provider,
        "rows": int(float(rows)),
        "market_share_pct": round(float(market_share_pct), 4)
    }


def save_provider_market_share():
    shares = provider_supply_share()

    FILE.parent.mkdir(parents=True, exist_ok=True)

    exists = FILE.exists()

    normalized = [
        _normalize_share_row(row)
        for row in shares
        if row.get("provider")
    ]

    with FILE.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "provider",
                "rows",
                "market_share_pct"
            ])

        ts = datetime.now(timezone.utc).isoformat()

        for row in normalized:
            writer.writerow([
                ts,
                row["provider"],
                row["rows"],
                row["market_share_pct"]
            ])

    return {
        "status": "saved",
        "file": str(FILE),
        "saved": len(normalized)
    }
