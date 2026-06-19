from pathlib import Path

ASSETS = [
    "data/live_offers/provider_live_offer_history.csv",
    "data/feature_store/daily_market_features.csv",
    "data/feature_store/gpu_market_depth_history.csv",
]

def intelligence_asset_registry():

    result = []

    for asset in ASSETS:

        path = Path(asset)

        result.append({
            "asset": asset,
            "exists": path.exists(),
            "size_bytes":
                path.stat().st_size
                if path.exists()
                else 0
        })

    return result
