from pathlib import Path

def asset_audit():

    files = [
        "data/live_offers/provider_live_offer_history.csv",
        "data/gpu_daily_state_history.csv",
        "data/provider_market_share_history.csv",
        "data/forecast_audit_history.csv",
        "data/forecast_snapshot_history.csv",
        "data/regime_history.csv"
    ]

    assets = []

    for file in files:

        p = Path(file)

        if not p.exists():
            continue

        assets.append({
            "file": file,
            "size_bytes": p.stat().st_size
        })

    return {
        "asset_count": len(assets),
        "assets": assets
    }
