from pathlib import Path

def asset_growth_tracker():

    files = [
        "data/live_offers/provider_live_offer_history.csv",
        "data/feature_store/gpu_market_depth_history.csv",
        "data/feature_store/daily_market_features.csv"
    ]

    return {
        f: (
            Path(f).stat().st_size
            if Path(f).exists()
            else 0
        )
        for f in files
    }
