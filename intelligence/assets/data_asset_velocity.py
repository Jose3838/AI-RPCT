from pathlib import Path

def data_asset_velocity():

    files = [
        "data/live_offers/provider_live_offer_history.csv",
        "data/forecast_audit_history.csv",
        "data/provider_coverage_history.csv"
    ]

    total = 0

    for f in files:

        p = Path(f)

        if p.exists():
            total += p.stat().st_size

    return {
        "tracked_bytes": total,
        "tracked_mb":
            round(
                total / 1024 / 1024,
                4
            )
    }
