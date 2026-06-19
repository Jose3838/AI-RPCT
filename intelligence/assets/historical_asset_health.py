import csv
from pathlib import Path


ASSETS = {
    "live_offer_history": "data/live_offers/provider_live_offer_history.csv",
    "daily_market_features": "data/feature_store/daily_market_features.csv",
    "gpu_market_depth_history": "data/feature_store/gpu_market_depth_history.csv",
    "provider_market_share_history": "data/provider_market_share_history.csv",
    "provider_dominance_regime_history": "data/provider_dominance_regime_history.csv",
    "forecast_snapshot_history": "data/forecast_snapshot_history.csv",
    "forecast_audit_history": "data/forecast_audit_history.csv",
    "regime_history": "data/regime_history.csv",
    "gpu_daily_state_history": "data/gpu_daily_state_history.csv",
    "live_coverage_history": "data/live_coverage_history.csv",
}


def _count_rows(path):
    file = Path(path)

    if not file.exists():
        return {
            "exists": False,
            "rows": 0,
            "status": "missing"
        }

    with file.open(newline="") as f:
        rows = list(csv.reader(f))

    data_rows = max(0, len(rows) - 1)

    if data_rows == 0:
        status = "empty"
    elif data_rows < 10:
        status = "thin"
    elif data_rows < 100:
        status = "growing"
    else:
        status = "healthy"

    return {
        "exists": True,
        "rows": data_rows,
        "status": status
    }


def historical_asset_health():
    assets = {}

    for name, path in ASSETS.items():
        health = _count_rows(path)
        health["file"] = path
        assets[name] = health

    existing = sum(1 for item in assets.values() if item["exists"])
    healthy = sum(1 for item in assets.values() if item["status"] == "healthy")
    growing = sum(1 for item in assets.values() if item["status"] in ["growing", "healthy"])
    missing = sum(1 for item in assets.values() if item["status"] == "missing")

    score = round(
        ((healthy * 1.0) + (growing * 0.6)) / max(len(assets), 1) * 100,
        2
    )

    return {
        "status": "ok",
        "asset_count": len(assets),
        "existing_assets": existing,
        "healthy_assets": healthy,
        "growing_or_healthy_assets": growing,
        "missing_assets": missing,
        "historical_asset_score": score,
        "assets": assets
    }
