from pathlib import Path
import csv


ASSETS = {
    "live_offer_history": "data/live_offers/provider_live_offer_history.csv",
    "forecast_audit_history": "data/forecast_audit_history.csv",
    "forecast_snapshot_history": "data/forecast_snapshot_history.csv",
    "forecast_accuracy_history": "data/forecast_accuracy_history.csv",
    "market_depth_history": "data/feature_store/gpu_market_depth_history.csv",
    "provider_market_share_history": "data/provider_market_share_history.csv",
    "provider_dominance_regime_history": "data/provider_dominance_regime_history.csv",
    "daily_market_features": "data/feature_store/daily_market_features.csv",
    "live_coverage_history": "data/live_coverage_history.csv",
    "regime_history": "data/regime_history.csv",
}


def _rows(file):
    path = Path(file)

    if not path.exists():
        return 0

    with path.open(newline="") as f:
        return max(0, len(list(csv.reader(f))) - 1)


def data_moat_score_v2():
    assets = {}

    for name, file in ASSETS.items():
        rows = _rows(file)

        if rows >= 1000:
            status = "strong"
        elif rows >= 100:
            status = "healthy"
        elif rows >= 10:
            status = "growing"
        elif rows > 0:
            status = "thin"
        else:
            status = "missing"

        assets[name] = {
            "file": file,
            "rows": rows,
            "status": status
        }

    live_rows = assets["live_offer_history"]["rows"]
    forecast_rows = assets["forecast_audit_history"]["rows"]
    accuracy_rows = assets["forecast_accuracy_history"]["rows"]

    asset_score = min(30, len([a for a in assets.values() if a["rows"] > 0]) * 3)
    history_score = min(25, live_rows / 1000 * 25)
    forecast_score = min(25, (forecast_rows / 100 * 15) + (accuracy_rows / 30 * 10))
    breadth_score = min(20, len([a for a in assets.values() if a["rows"] >= 10]) * 3)

    score = round(
        asset_score + history_score + forecast_score + breadth_score,
        2
    )

    if score >= 80:
        level = "strong_data_moat"
    elif score >= 60:
        level = "growing_data_moat"
    elif score >= 35:
        level = "early_data_moat"
    else:
        level = "weak_data_moat"

    return {
        "status": "ok",
        "version": "v2",
        "data_moat_score": score,
        "data_moat_level": level,
        "components": {
            "asset_score": round(asset_score, 2),
            "history_score": round(history_score, 2),
            "forecast_score": round(forecast_score, 2),
            "breadth_score": round(breadth_score, 2)
        },
        "assets": assets
    }
