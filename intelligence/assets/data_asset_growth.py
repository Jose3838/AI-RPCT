from pathlib import Path

def data_asset_growth():

    files = [
        "data/live_offers/provider_live_offer_history.csv",
        "data/feature_store/daily_market_features.csv",
        "data/feature_store/gpu_market_depth_history.csv",
        "data/forecast_snapshot_history.csv"
    ]

    total = 0

    for f in files:

        p = Path(f)

        if p.exists():
            total += p.stat().st_size

    return {
        "asset_size_bytes": total,
        "asset_size_mb":
            round(
                total / 1024 / 1024,
                4
            )
    }
