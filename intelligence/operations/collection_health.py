from pathlib import Path

FILES = [
    "data/live_offers/provider_live_offer_history.csv",
    "data/gpu_daily_state_history.csv",
    "data/provider_market_share_history.csv",
    "data/forecast_audit_history.csv"
]

def collection_health():

    missing = []

    for file in FILES:

        if not Path(file).exists():
            missing.append(file)

    return {
        "healthy": len(missing) == 0,
        "missing": missing
    }
