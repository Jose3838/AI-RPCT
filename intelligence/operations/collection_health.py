from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

OFFER_HISTORY = "data/live_offers/provider_live_offer_history.csv"

REQUIRED_FILES = [
    "data/live_offers/provider_live_offer_history.csv",
    "data/gpu_daily_state_history.csv",
    "data/provider_market_share_history.csv",
    "data/forecast_audit_history.csv"
]


def collection_health(minutes=10):

    missing = [
        file for file in REQUIRED_FILES
        if not Path(file).exists()
    ]

    if not Path(OFFER_HISTORY).exists():
        return {
            "status": "missing_offer_history",
            "healthy": False,
            "missing": missing,
            "rows": 0,
            "latest_snapshot_rows": 0,
            "providers_reporting": 0,
            "minutes_since_last_collection": None
        }

    df = pd.read_csv(OFFER_HISTORY)

    if df.empty:
        return {
            "status": "empty_offer_history",
            "healthy": False,
            "missing": missing,
            "rows": 0,
            "latest_snapshot_rows": 0,
            "providers_reporting": 0,
            "minutes_since_last_collection": None
        }

    df["observed_at"] = pd.to_datetime(
        df["observed_at"],
        errors="coerce",
        utc=True
    )

    df = df.dropna(
        subset=["observed_at", "provider"]
    )

    latest_time = df["observed_at"].max()
    now = datetime.now(timezone.utc)

    window_start = latest_time - pd.Timedelta(
        minutes=minutes
    )

    latest = df[
        df["observed_at"] >= window_start
    ]

    latest_snapshot_rows = int(len(latest))
    providers_reporting = int(latest["provider"].nunique())

    minutes_since_last_collection = round(
        (now - latest_time.to_pydatetime()).total_seconds() / 60,
        2
    )

    if missing:
        status = "incomplete"
    elif minutes_since_last_collection > 90:
        status = "stale"
    elif latest_snapshot_rows < 5:
        status = "weak_snapshot"
    elif providers_reporting < 2:
        status = "low_provider_coverage"
    else:
        status = "healthy"

    return {
        "status": status,
        "healthy": status == "healthy",
        "missing": missing,
        "rows": int(len(df)),
        "latest_snapshot_rows": latest_snapshot_rows,
        "providers_reporting": providers_reporting,
        "minutes_since_last_collection": minutes_since_last_collection,
        "latest_observed_at": latest_time.isoformat(),
        "window_minutes": minutes
    }
