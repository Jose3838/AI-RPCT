from pathlib import Path

FILES = [
    "data/live_offers/provider_live_offer_history.csv",
    "data/feature_store/daily_market_features.csv",
    "data/feature_store/gpu_market_depth_history.csv",
]

def historical_asset_audit():

    total_bytes = 0

    for file in FILES:

        p = Path(file)

        if p.exists():
            total_bytes += p.stat().st_size

    return {
        "asset_bytes":
            total_bytes
    }
