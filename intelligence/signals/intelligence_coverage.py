from pathlib import Path

def intelligence_coverage():

    assets = [
        "data/live_offers/provider_live_offer_history.csv",
        "data/feature_store/daily_market_features.csv",
        "data/feature_store/gpu_market_depth_history.csv",
        "data/executive_intelligence_history.csv"
    ]

    available = sum(
        Path(a).exists()
        for a in assets
    )

    return {
        "coverage":
            round(
                available / len(assets),
                4
            )
    }
